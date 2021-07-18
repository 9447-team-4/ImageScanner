"""

Contains common interfaces for reporters

"""
from typing import List
import json


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

    @property
    def __dict__(self):
        return json.loads(
            json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        )

    @property
    def __str__(self):
        return json.dumps(self.__dict__)


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
    def __dict__(self):
        return json.loads(
            json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        )

    @property
    def __str__(self):
        return json.dumps(self.__dict__)


class Issue:

    def __init__(self, name, description, labels: List[Label]):
        self._name = name
        self._description = description
        self._labels = labels

    @property
    def name(self):
        return self._color

    @name.setter
    def name(self, name):
        self._name = name

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

    @property
    def __dict__(self) -> str:
        return json.loads(
            json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        )

    @property
    def __str__(self):
        return json.dumps(self.__dict__)


class GitService:
    """
    An interface to interact with various Git services
    For example, It provides functionalities to get issues, set issues and also get PR information
    """

    def __init__(self, repo: str, user: str, token: str):
        self.authenticate(user, token)
        self._user = user
        self._repo = repo

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

    def report_issues(self):
        """
        Report issues to the Git service
        """

        if len(self._issues) == 0:
            raise Exception('Cannot report empty list of issues')

        self._git_service.add_issues(self._issues)
