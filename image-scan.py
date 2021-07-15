#!/usr/bin/env python3
import argparse
import json
from git import Repo
from functools import reduce
from typing import List

import os
import giteapy
from dotenv import load_dotenv

load_dotenv()

# Configure API key authorization: AccessToken
configuration = giteapy.Configuration()
configuration.api_key['access_token'] = os.getenv('GITEA_TOKEN')

# Setting the client api with custom host to be the default api
configuration.host = f"http://{os.getenv('GITEA_HOST')}:{os.getenv('GITEA_PORT')}/api/v1"
api_client = giteapy.ApiClient(configuration=configuration)

configuration = giteapy.Configuration()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Vulnerability:
    def __init__(self, title, severity, references=None):
        self.title = title
        self.severity = severity
        self.references = references

    def __attrs(self):
        return self.title

    def __eq__(self, other):
        return isinstance(other, Vulnerability) and self.__attrs() == other.__attrs()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__attrs())


class VulnReporterInterface:
    """
    An interface which defines how the vulnerabilities 
    are stored: Could be stored in a file, an S3 bucket, or a database or it could even be an API to some issue tracker
    """

    def get_vulns(self, **kwargs) -> List[Vulnerability]:
        """
        Returns a json list of vulnerabilities currently in hold for a branch
        """
        pass

    def store_vulns(self, vulns: List[Vulnerability], **kwargs) -> None:
        """
        Stores a vulnerability in the store
        """
        pass


def generate_reporter(git_service) -> VulnReporterInterface:
    if git_service == 'gitea':
        return GiteaReporter(giteapy.api_client)


class GiteaReporter(VulnReporterInterface):

    def __init__(self, api_client):
        self._api_client = api_client
        self._issues_api = giteapy.IssueApi(giteapy.api_client)
        self._owner = os.getenv('GITEA_USERNAME')
        self._repo = os.getenv('GITEA_REPO')

    def get_vulns(self, **kwargs) -> List[Vulnerability]:
        """
            Accessing the authenticated Gitea api client 
            and listing all the issues that exist there
        """

        issues = self._issues_api.issue_list_issues(self._owner, self._repo)
        labels = list(map(lambda x: x.labels, issues))

        # Filter issues which are not vulnerabilities
        severities = ['low vulnerability',
                      'medium vulnerability', 'high vulnerability']

        combined = []
        for l, i in zip(labels, issues):
            if set([lab.name for lab in l]).intersection(severities):
                combined.append((l[0], i))

        return list(map(lambda x: Vulnerability(x[1].title, x[0].name, x[1].body), combined))

    def store_vulns(self, vulns: List[Vulnerability], **kwargs) -> None:
        """
            Creating a new issue containing the vulnerabilities found on Gitea
        """
        colors = {
            'high': 'ff0000',
            'medium': 'ffa500',
            'low': 'ffff00'
        }

        for v in vulns:
            # Create an label for its vulnerability severity

            label_name = f'{v.severity} vulnerability'

            label_id = self.label_exists(label_name)

            if not label_id:
                label_opt = giteapy.models.CreateLabelOption(
                    color=colors[v.severity], name=label_name)

                label_id = self._issues_api.issue_create_label(
                    owner=self._owner, repo=self._repo, body=label_opt).id

            # Create issue for it
            cio = giteapy.models.CreateIssueOption(
                body=json.dumps(v.references, indent=1), title=v.title, labels=[label_id])

            self._issues_api.issue_create_issue(
                owner=self._owner, repo=self._repo, body=cio)

    def label_exists(self, label):
        """
            Check whether a label exists so we don't have to create them again. If it does
            exist then return its id, otherwise return None
        """
        labels = self._issues_api.issue_list_labels(
            owner=self._owner, repo=self._repo)
        for l in labels:
            if l.name == label:
                return l.id
        return None


def open_repo(repopath):
    return Repo(repopath)


def diff_reports(*reports):
    """
        Check if the reports have different vulnerabilities,
        Returns a set of all vulnerabilities that do not exist in all reports

    """
    all_vulns = list()

    for report in reports:
        report_vulns = set()
        for entry in report['vulnerabilities']:

            report_vulns.add(entry['id'])
        all_vulns.append(report_vulns)

    vulns_set = reduce(lambda s, l: l | s, all_vulns, set())

    # difference in vulns w.r.t each report
    diff_vulns = list(map(lambda s: vulns_set - s, all_vulns))
    return diff_vulns


def scan_branches(repo, *branches):
    """
        Generate reports for the dockerfiles existing in all branches
        returns: list of json reports
    """

    for branch in branches:
        repo.heads[branch].checkout()

        repopath = repo.working_tree_dir
        dockerfile = repopath + '/Dockerfile'
        print(bcolors.OKGREEN + 'Building the image on branch ' +
              bcolors.WARNING + branch + bcolors.ENDC + '...')
        os.system(
            f'docker build -t image-scan -f {dockerfile} {repopath} > /dev/null')
        print(bcolors.OKGREEN + 'Scanning image on branch ' +
              bcolors.WARNING + branch + bcolors.ENDC + '...')
        json_out = os.popen(
            f"docker scan --json --group-issues --file {dockerfile} image-scan").read()
        yield json.loads(json_out)


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def submitIssue(vulns, reporter):
    """
        Send an api request to target to submit an issue for the vulnerability

        :param vulns: a list of new vulnerabilities to submit as issues.
    """

    new_vulns = set(list(map(lambda x: Vulnerability(
        x.get('title'), x.get('severity'), x.get('references')), vulns)))
    old_vulns = set(reporter.get_vulns())

    to_submit = new_vulns - old_vulns

    reporter.store_vulns(to_submit)


def scan(repopath, severity, branch):
    """
        Scan a repo's dockerfile for any vulnerabilities.
        returns: a list of vulnerabilities 
    """

    repo = open_repo(repopath)

    json_result = next(scan_branches(repo, branch))

    def fil(x): return x['severity'] in severity

    vuln_list = list(filter(fil, json_result['vulnerabilities']))

    return vuln_list


def compare(repopath, severity, target, base):
    """
        Returns a list of new vulnerabilities introduced to 
        target branch.
    """
    repo = open_repo(repopath)

    # this returns a list of vulnerabilities that does not exist in
    # the branch itself. So the ideal case is that both list of
    # vulnerabilities are the same, which means the base branch
    # is not introducing any new vulnerabilities
    report_target, report_base = scan_branches(repo, target, base)

    def fil(x): return x['severity'] in severity

    report_target['vulnerabilities'] = list(
        filter(fil, report_target['vulnerabilities']))
    report_base['vulnerabilities'] = list(
        filter(fil, report_base['vulnerabilities']))
    [diff_vulns_target, _] = diff_reports(report_target, report_base)

    return diff_vulns_target


if __name__ == "__main__":

    parser = argparse.ArgumentParser('image-scan')

    subparsers = parser.add_subparsers(dest='subcommand')

    parser_scan = subparsers.add_parser(
        'scan', help="Scan a branch's Dockerfile for vulnerabilities")

    parser_scan.add_argument(
        '--severity',
        default='low',
        choices=['low', 'medium', 'high'],
        help='The lowest severity you want to detect')

    parser_scan.add_argument('branch', help='The branch you want to scan')
    parser_scan.add_argument('--git_service', choices=['github', 'bitbucket', 'gitlab', 'gitea'],
                             help='The git service you to want to report the vulnerability to.',
                             default='gitea')

    parser_compare = subparsers.add_parser(
        'compare', help="Compare two branches for vulnerabilities")

    parser_compare.add_argument(
        '--severity',
        nargs=1, default='low',
        choices=['low', 'medium', 'high'],
        help='The lowest severity you want to consider while comparing')

    parser_compare.add_argument(
        'target_branch',
        help='The target branch you want in to compare with.')

    parser_compare.add_argument(
        'base_branch',
        help='The base branch you want to compare with.')

    parser.add_argument('repo', type=dir_path,
                        help='The path to the repo that contains a Dockerfile')

    args = parser.parse_args()

    severity = []
    if args.severity:
        if args.severity == 'high':
            severity.append('high')
        elif args.severity == 'medium':
            severity.extend(['high', 'medium'])
        else:
            severity.extend(['high', 'medium', 'low'])

    if args.subcommand == 'scan':
        vulns = scan(args.repo, severity, args.branch)

        if vulns:
            print(bcolors.WARNING +
                  f'Found vulnerabilities: {json.dumps(vulns, indent=4)}' + bcolors.ENDC)

            submitIssue(vulns, generate_reporter(args.git_service))
            exit(1)

    elif args.subcommand == 'compare':
        target, base = args.target_branch, args.base_branch
        result = compare(args.repo, severity, target, base)
        if result:
            print(
                bcolors.FAIL + f'Branch {base} is introducing new vulnerabilities to branch {target}!')
            print(f'Vulnerabilities found: {result}' + bcolors.ENDC)
            exit(1)

    print(bcolors.OKGREEN + 'No new vulnerabilities detected' + bcolors.ENDC)
