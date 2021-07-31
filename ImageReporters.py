from Reporters import PullRequestReporter, IssueReporter, Issue, Label, PullReview, GitService
from enum import Enum
from typing import List, Dict
import os
import subprocess

import json
import ast
from parse import parse
from collections import Counter


class Severity(Enum):
    low = 1,
    medium = 2,
    high = 3,
    critical = 4,


class Reference(object):
    def __init__(self, title: str, url: str):
        self._title = title
        self._url = url

    @property
    def title(self):
        return self._title

    @property
    def url(self):
        return self._url

    def to_dict(self) -> Dict:
        return json.loads(
            json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        )

    @staticmethod
    def from_dict(reference_dict: Dict):
        """
        Parse from a dictionary object
        """
        return Reference(**reference_dict)

    @staticmethod
    def from_json(json_str: str):
        """
        Parse from json string
        """
        reference_dict = json.loads(json_str)
        return Reference.from_dict(reference_dict)

    def __hash__(self):
        json_str = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)), sort_keys=True)
        return hash(json_str)

    def __str__(self):
        return json.dumps({'_title': self.title, '_url': self.url})


class Vulnerability:
    colors: Dict[Severity, str] = {
        Severity.low: 'ffff00',
        Severity.medium: 'ffa500',
        Severity.high: 'f32013',
        Severity.critical: 'a1045a'
    }

    def __init__(self, id: str, title: str, severity: Severity, references: List[Reference] = None):
        self._id = id
        self._title = title
        self._severity = severity
        self._references = references

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def severity(self):
        return self._severity

    @property
    def references(self):
        return self._references

    def to_dict(self) -> Dict:
        return json.loads(
            json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        )

    def to_issue(self) -> Issue:
        title = f'{self.title} ({self.id})'

        references_dicts = list(map(lambda x: x.to_dict(), self.references))
        labels = [Label(self.severity.name, Vulnerability.colors[self.severity])]
        return Issue(title, self._prettify_references(), labels)

    @staticmethod
    def from_issue(issue: Issue):
        title, id = parse('{} ({})', issue.title)

        references = None
        if issue.description:
            references = Vulnerability._parse_references_from_issue(issue.description)

        if len(issue.labels) > 1:
            raise Exception('Cannot parse Vulnerability: Issue has multiple labels! ')

        severity = Severity[issue.labels[0].name]

        return Vulnerability(id, title, severity, references)

    @staticmethod
    def from_dict(vuln_dict: Dict):
        references = list(map(lambda x: Reference.from_dict(x), vuln_dict['references']))
        vuln_dict['references'] = references
        return Vulnerability(**vuln_dict)

    def __eq__(self, other):
        if not isinstance(other, Vulnerability):
            return False

        vuln_dict = self.to_dict()
        # Sort the array objects
        vuln_dict['_references'].sort(key=lambda k: (k['_title'], k['_url']))
        other_dict = other.to_dict()
        # Sort the array objects
        other_dict['_references'].sort(key=lambda k: (k['_title'], k['_url']))
        return vuln_dict == other_dict

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        vuln_dict = self.to_dict()
        # Sort the array objects
        vuln_dict['_references'].sort(key=lambda k: (k['_title'], k['_url']))
        return hash(json.dumps(vuln_dict, sort_keys=True))

    def _prettify_references(self):

        if not self.references:
            return '# No references found'

        result = '# References\n'
        result += '--------------------------------\n'
        for ref in self.references:
            result += f'### Title: {ref.title}\n'
            result += f'### URL: {ref.url}\n'
            result += f'--------------------------------\n'

        return result

    @staticmethod
    def _parse_references_from_issue(description):
        """
        Parse references from the markdown description (issue description
        @param description: Issue description
        @return: List[Reference]
        """

        if description == '# No references found':
            return list()

        if description[0] != '#':
            return list()

        lines = description.split('\n')

        references = list()
        for i in range(2, len(lines) - 1, 3):
            title = parse('### Title: {}', lines[i])
            url = parse('### URL: {}', lines[i + 1])
            references.append(Reference(title, url))

        return references


def parse_reference(x):
    return {
        'title': x.get('title'),
        'url': x.get('url'),
    }


def parse_vuln(x):
    return {
        'id': x.get('id'),
        'title': x.get('title'),
        'severity': Severity[x.get('severity')],
        'references': list(map(parse_reference, x.get('references', [])))
    }


def scan(image_tag: str, snyk_token: str, severity: Severity) -> List[Vulnerability]:
    """
    Use snyk cli to scan image for vulnerabilities
    @param image_tag: the image you want to scan
    @param snyk_token: snyk api token
    @param severity: severity threshold
    @return: a list of vulnerabilities
    """
    os.system(f'snyk config set api={snyk_token}')

    p = subprocess.Popen(f'snyk container test {image_tag} --severity-threshold={severity.name} --json', \
                         shell=True, stdout=subprocess.PIPE)
    stdout, _ = p.communicate()

    vulns_dict = json.loads(stdout)
    if p.returncode == 2 or p.returncode == 3:
        raise Exception(f'snyk: Could not scan {image_tag}; e.what(): {vulns_dict["error"]}')

    return list(map(lambda v: Vulnerability.from_dict(parse_vuln(v)), vulns_dict['vulnerabilities']))


class ImageIssueReporter(IssueReporter):
    """
    A class that reports image vulnerabilities found on the main branch as issues.
    """

    def __init__(self, git_service: GitService, snyk_token: str, image_tag: str, severity: Severity = Severity.low):
        super(ImageIssueReporter, self).__init__(git_service)
        self._snyk_token = snyk_token
        self._image_tag = image_tag
        self._severity = severity
        self._new_vulnerabilites: List[Vulnerability] = list()

    @property
    def new_vulnerabilites(self):
        return self._new_vulnerabilites

    def process_issues(self):
        """
        Scan vulnerabilities, create issues out of them, and check if such issues already exist
        before submitting them
        @return: None
        """

        vulns = scan(self._image_tag, self._snyk_token, self._severity)

        issues = list(map(lambda v: v.to_issue(), vulns))

        old_issues = self.git_service.get_issues()

        new_issues = set(issues) - set(old_issues)

        self.issues = new_issues
        self._new_vulnerabilites = list(map(Vulnerability.from_issue, new_issues))


class ImagePRReporter(PullRequestReporter):
    """
    A class that reports image vulnerabilities introduced by base branch (feature) to target branch
    (main or master)
    """

    def __init__(self, git_service: GitService, pr_id: int, snyk_token: str, base_image: str, \
                 target_image: str, severity: Severity = Severity.low):
        super(ImagePRReporter, self).__init__(git_service, pr_id)

        self._snyk_token = snyk_token
        self._base_image = base_image
        self._target_image = target_image
        self._severity = severity

        self._exit_status = 0
        self._new_vulnerabilities: List[Vulnerability] = list()

    @property
    def new_vulnerabilites(self):
        return self._new_vulnerabilities

    @property
    def exit_status(self):
        return self._exit_status

    def process_pull_review(self):
        """
        Scan two branches, find if there are any new vulnerabilties introduced, and report them back
        @return: None
        """

        base_vulns = scan(self._base_image, self._snyk_token, self._severity)
        target_vulns = scan(self._target_image, self._snyk_token, self._severity)

        new_vulns = set(base_vulns) - set(target_vulns)

        result = 'No New Vulnerabilities.\n'
        if len(new_vulns) > 0:
            result = '# Found Image Vulnerabilities: \n'
            self._exit_status = 1

        # counting vulnerabilities of each severity
        severities = list(map(lambda x: x.severity.name, new_vulns))
        severities_count = Counter(severities)

        # Filter out critical vulnerabilties, if any
        critical_vulns = list(filter(lambda x: x.severity == Severity.critical, new_vulns))
        for critical_vuln in critical_vulns:
            result += '## Critical:\n'
            result += f'### Title: {critical_vuln.title}\n'
            if critical_vuln.references:
                result += f'### Information:\n'
                result += f'##### URL: {critical_vuln.references[0].url}\n'
                result += f'---------------------------------------------------------------------------\n'

        self._new_vulnerabilites = list(new_vulns)

        if severities_count:
            result += "# Statistics\n" \
                     "| Risk Level\t\t | Amount of Vulnerabilities |\n" \
                     "| -------------- | ------------------------- |\n"
            for severity, count in sorted(severities_count.items()):
                result += f"| {severity}\t\t | {count}                    |\n" \

        result += '\n---------------------------------------------------------------------------\n'
        self.pull_review.body = result
