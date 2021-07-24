"""

Contains common interfaces for reporters

"""
from typing import List, Dict
import json
import giteapy


class PullReview:
    """
    A pull request review (or comment object)
    """

    def __init__(self, pr_id: int, body: str = ''):
        self._pr_id = pr_id
        self._body = body

    @property
    def pr_id(self):
        return self._pr_id

    @pr_id.setter
    def pr_id(self, pr_id: int):
        self._pr_id = pr_id

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body: str):
        self._body = body

    def to_dict(self):
        return json.loads(
            json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        )


class Label:

    def __init__(self, name, color):
        self._name = name
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    def to_dict(self):
        return json.loads(
            json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        )

    def __eq__(self, other):

        if not isinstance(other, Issue):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        if not isinstance(other, Issue):
            return False

        return self.to_dict() != other.to_dict()

    @staticmethod
    def from_dict(label_dict: Dict):
        """
        Parse from a dictionary object
        """
        return Label(**label_dict)

    @staticmethod
    def from_json(json_str: str):
        """
        Parse from json string
        """
        label_dict = json.loads(json_str)
        return Label.from_dict(label_dict)

    def __hash__(self):
        json_str = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)), sort_keys=True)
        return hash(json_str)


class Issue:

    def __init__(self, title, description, labels: List[Label]):
        self._title = title
        self._description = description
        self._labels = labels

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def labels(self):
        return list(self._labels)

    @labels.setter
    def labels(self, labels):
        self._labels = labels

    def to_dict(self) -> Dict:
        return json.loads(
            json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        )

    def __eq__(self, other):

        if not isinstance(other, Issue):
            return False

        issue_dict = self.to_dict()
        # Sort the array objects
        issue_dict['_labels'].sort(key=lambda k: (k['_name'], k['_color']))
        other_dict = other.to_dict()
        # Sort the array objects
        other_dict['_labels'].sort(key=lambda k: (k['_name'], k['_color']))
        return issue_dict == other_dict

    def __ne__(self, other):
        if not isinstance(other, Issue):
            return False

        issue_dict = self.to_dict()
        # Sort the array objects
        issue_dict['_labels'].sort(key=lambda k: (k['_name'], k['_color']))
        other_dict = self.to_dict()
        # Sort the array objects
        other_dict['_labels'].sort(key=lambda k: (k['_name'], k['_color']))
        return issue_dict != other_dict

    def __hash__(self):
        issue_dict = self.to_dict()
        # Sort the array objects
        issue_dict['_labels'].sort(key=lambda k: (k['_name'], k['_color']))
        return hash(json.dumps(issue_dict, sort_keys=True))

    @staticmethod
    def from_dict(issue_dict: Dict):
        labels = list(map(lambda x: Label.from_dict(x), issue_dict['labels']))
        issue_dict['labels'] = labels
        return Issue(**issue_dict)

    @staticmethod
    def from_json(self, json_str: str):
        """
        Parse from json string
        """
        issue_dict = json.loads(json_str)
        return self.from_dict(issue_dict)


class GitService:
    """
    An interface to interact with various Git services
    For example, It provides functionalities to get issues, set issues and also get PR information
    """

    def __init__(self, repo: str, user: str, token: str, host: str, port: str):
        self._user = user
        self._repo = repo
        self._host = host
        self._port = port
        self.authenticate(user, token)

    def get_issues(self) -> List[Issue]:
        """
        Return a list of issues  from the repository

        :returns: List[Issue]
        """
        pass

    def add_issues(self, issues: List[Issue]) -> None:
        """
        Add issues to the the git interface. Issues with a name that exists will be ignored...

        :param issues: List of Issue objects: List[Issue]
        """
        pass

    def add_pr_review(self, pr_review: PullReview) -> None:
        """
        Add a pull review (comment) on a pull request
        """
        pass

    def authenticate(self, repo: str, user: str, token: str):
        """
        Authenticate with the Git service using token based authentication

        :param repo: The name of the repo to gain access to
        :param user: The user under which the login is going to happen. Has to be authorized to access repo
        :param token: Authentication token
        """
        pass

    @property
    def user(self):
        return self._user

    @property
    def repo(self):
        return self._repo


class PullRequestReporter:
    """
    A pull request reporter that reports whatever information
    into a review on a pull request
    """

    def __init__(self, git_service: GitService, pr_id: int):
        self._git_service = git_service
        self._pr_id = pr_id
        self._pull_review = PullReview(pr_id, '')

    @property
    def pull_review(self):
        return self._pull_review

    @pull_review.setter
    def pull_review(self, pull_review: PullReview):
        self._pull_review = pull_review

    @property
    def git_service(self):
        return self._git_service

    @git_service.setter
    def git_service(self, git_service: GitService):
        self._git_service = git_service

    def process_pull_review(self):
        """
        Process a pull review before submitting.

        Here you need to add logic based on what kind of thing you are reporting: Static Analysis, Fuzzing, etc...
        """
        pass

    def commit_review(self):
        """
        Commit review to git service once processing has been done
        """
        if self._pull_review.body == '':
            raise Exception('You cannot submit an empty pull review!')

        self._git_service.add_pr_review(self._pull_review)


class IssueReporter:
    """
    An interface for reporting any stage of the pipeline as issues inside on the Git service.
    For example, to report image vulnerability periodic scans
    """

    def __init__(self, git_service: GitService):
        self._git_service = git_service
        self._issues = []

    @property
    def issues(self):
        return self._issues

    @issues.setter
    def issues(self, issues: List[Issue]):
        self._issues = issues

    @property
    def git_service(self):
        return self._git_service

    @git_service.setter
    def git_service(self, git_service: GitService):
        self._git_service = git_service

    def process_issues(self):
        """
        Perform any processing for issues before reporting to the Git service.
        """
        pass

    def commit_issues(self):
        """
        Report issues to the Git service
        """

        if len(self._issues) == 0:
            raise Exception('Cannot report empty list of issues')

        self._git_service.add_issues(self._issues)


class GiteaService(GitService):
    """
    A Gitea service
    """

    def __init__(self, *kwargs):
        self._configuration = giteapy.Configuration()
        self._api_client = None
        self._issue_api = None
        self._repo_api = None
        super(GiteaService, self).__init__(*kwargs)

    def authenticate(self, user: str, token: str):
        self._configuration.api_key['access_token'] = token
        self._configuration.host = f"http://{self._host}:{self._port}/api/v1"
        self._api_client = giteapy.ApiClient(configuration=self._configuration)
        self._issue_api = giteapy.IssueApi(self._api_client)
        self._repo_api = giteapy.RepositoryApi(self._api_client)

    @staticmethod
    def _parse_label(x):
        return {
            'name': x.name,
            'color': x.color
        }

    @staticmethod
    def _parse_issue(x):
        return {
            'title': x.title,
            'description': x.body,
            'labels': list(map(GiteaService._parse_label, x.labels))
        }

    def get_issues(self) -> List[Issue]:
        issues = self._issue_api.issue_list_issues(self._user, self._repo)

        return list(map(lambda x: Issue.from_dict(GiteaService._parse_issue(x)), issues))

    @staticmethod
    def _find_label_ids(label, labels):
        """
        Private method to fetch label id given its name and color
        @param label: Label object
        @param labels: Gitea API Label object
        @return: number representing label id, None if not found
        """
        for l in labels:
            if l.name == label.name and l.color == label.color:
                return l.id
        return None

    def add_issues(self, issues: List[Issue]) -> None:
        """
        Add new Issues to Gitea issue board. Will only add issues that have not been stored before.
        @param issues: A list of issues to be added
        @return: None
        """

        # Get the new and unique issues
        old_issues = self.get_issues()
        old_issues_s = set(old_issues)
        issues_s = set(issues)
        new_issues_s = issues_s - old_issues_s

        parse_label = lambda x: Label.from_dict({
            'name': x.name,
            'color': x.color
        })

        # Get all possible labels
        gitea_labels = self._issue_api.issue_list_labels(self._user, self._repo)
        labels = set(list(map(parse_label, gitea_labels)))

        # Send new issues to Gitea
        for issue in new_issues_s:
            label_ids = []
            for label in issue.labels:
                # If the label does not exist, create it
                if label not in labels:
                    label_opt = giteapy.models.CreateLabelOption(color=label.color, name=label.name)
                    label_id = self._issue_api.issue_create_label(
                        owner=self._user, repo=self._repo, body=label_opt).id
                # Find its label id
                else:
                    label_id = self._find_label_ids(label, gitea_labels)
                label_ids.append(label_id)

            # Create issues finally :D
            cio = giteapy.models.CreateIssueOption(
                body=issue.description, title=issue.title, labels=label_ids)

            self._issue_api.issue_create_issue(
                owner=self._user, repo=self._repo, body=cio)

    def add_pr_review(self, pr_review: PullReview) -> None:
        """
        Create a PR pull review in Gitea
        @param pr_review: PullReview object
        @return: None
        """
        opt = giteapy.models.CreatePullReviewOptions(body=pr_review.body)
        self._repo_api.repo_create_pull_review(repo=self._repo, owner=self._user, index=pr_review.pr_id, body=opt)
