# coding: utf-8

"""
    Gitea API.

    This documentation describes the Gitea API.  # noqa: E501

    OpenAPI spec version: 1.15
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from swagger_client.configuration import Configuration


class EditRepoOption(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'allow_manual_merge': 'bool',
        'allow_merge_commits': 'bool',
        'allow_rebase': 'bool',
        'allow_rebase_explicit': 'bool',
        'allow_squash_merge': 'bool',
        'archived': 'bool',
        'autodetect_manual_merge': 'bool',
        'default_branch': 'str',
        'default_merge_style': 'str',
        'description': 'str',
        'external_tracker': 'ExternalTracker',
        'external_wiki': 'ExternalWiki',
        'has_issues': 'bool',
        'has_projects': 'bool',
        'has_pull_requests': 'bool',
        'has_wiki': 'bool',
        'ignore_whitespace_conflicts': 'bool',
        'internal_tracker': 'InternalTracker',
        'mirror_interval': 'str',
        'name': 'str',
        'private': 'bool',
        'template': 'bool',
        'website': 'str'
    }

    attribute_map = {
        'allow_manual_merge': 'allow_manual_merge',
        'allow_merge_commits': 'allow_merge_commits',
        'allow_rebase': 'allow_rebase',
        'allow_rebase_explicit': 'allow_rebase_explicit',
        'allow_squash_merge': 'allow_squash_merge',
        'archived': 'archived',
        'autodetect_manual_merge': 'autodetect_manual_merge',
        'default_branch': 'default_branch',
        'default_merge_style': 'default_merge_style',
        'description': 'description',
        'external_tracker': 'external_tracker',
        'external_wiki': 'external_wiki',
        'has_issues': 'has_issues',
        'has_projects': 'has_projects',
        'has_pull_requests': 'has_pull_requests',
        'has_wiki': 'has_wiki',
        'ignore_whitespace_conflicts': 'ignore_whitespace_conflicts',
        'internal_tracker': 'internal_tracker',
        'mirror_interval': 'mirror_interval',
        'name': 'name',
        'private': 'private',
        'template': 'template',
        'website': 'website'
    }

    def __init__(self, allow_manual_merge=None, allow_merge_commits=None, allow_rebase=None, allow_rebase_explicit=None, allow_squash_merge=None, archived=None, autodetect_manual_merge=None, default_branch=None, default_merge_style=None, description=None, external_tracker=None, external_wiki=None, has_issues=None, has_projects=None, has_pull_requests=None, has_wiki=None, ignore_whitespace_conflicts=None, internal_tracker=None, mirror_interval=None, name=None, private=None, template=None, website=None, _configuration=None):  # noqa: E501
        """EditRepoOption - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._allow_manual_merge = None
        self._allow_merge_commits = None
        self._allow_rebase = None
        self._allow_rebase_explicit = None
        self._allow_squash_merge = None
        self._archived = None
        self._autodetect_manual_merge = None
        self._default_branch = None
        self._default_merge_style = None
        self._description = None
        self._external_tracker = None
        self._external_wiki = None
        self._has_issues = None
        self._has_projects = None
        self._has_pull_requests = None
        self._has_wiki = None
        self._ignore_whitespace_conflicts = None
        self._internal_tracker = None
        self._mirror_interval = None
        self._name = None
        self._private = None
        self._template = None
        self._website = None
        self.discriminator = None

        if allow_manual_merge is not None:
            self.allow_manual_merge = allow_manual_merge
        if allow_merge_commits is not None:
            self.allow_merge_commits = allow_merge_commits
        if allow_rebase is not None:
            self.allow_rebase = allow_rebase
        if allow_rebase_explicit is not None:
            self.allow_rebase_explicit = allow_rebase_explicit
        if allow_squash_merge is not None:
            self.allow_squash_merge = allow_squash_merge
        if archived is not None:
            self.archived = archived
        if autodetect_manual_merge is not None:
            self.autodetect_manual_merge = autodetect_manual_merge
        if default_branch is not None:
            self.default_branch = default_branch
        if default_merge_style is not None:
            self.default_merge_style = default_merge_style
        if description is not None:
            self.description = description
        if external_tracker is not None:
            self.external_tracker = external_tracker
        if external_wiki is not None:
            self.external_wiki = external_wiki
        if has_issues is not None:
            self.has_issues = has_issues
        if has_projects is not None:
            self.has_projects = has_projects
        if has_pull_requests is not None:
            self.has_pull_requests = has_pull_requests
        if has_wiki is not None:
            self.has_wiki = has_wiki
        if ignore_whitespace_conflicts is not None:
            self.ignore_whitespace_conflicts = ignore_whitespace_conflicts
        if internal_tracker is not None:
            self.internal_tracker = internal_tracker
        if mirror_interval is not None:
            self.mirror_interval = mirror_interval
        if name is not None:
            self.name = name
        if private is not None:
            self.private = private
        if template is not None:
            self.template = template
        if website is not None:
            self.website = website

    @property
    def allow_manual_merge(self):
        """Gets the allow_manual_merge of this EditRepoOption.  # noqa: E501

        either `true` to allow mark pr as merged manually, or `false` to prevent it. `has_pull_requests` must be `true`.  # noqa: E501

        :return: The allow_manual_merge of this EditRepoOption.  # noqa: E501
        :rtype: bool
        """
        return self._allow_manual_merge

    @allow_manual_merge.setter
    def allow_manual_merge(self, allow_manual_merge):
        """Sets the allow_manual_merge of this EditRepoOption.

        either `true` to allow mark pr as merged manually, or `false` to prevent it. `has_pull_requests` must be `true`.  # noqa: E501

        :param allow_manual_merge: The allow_manual_merge of this EditRepoOption.  # noqa: E501
        :type: bool
        """

        self._allow_manual_merge = allow_manual_merge

    @property
    def allow_merge_commits(self):
        """Gets the allow_merge_commits of this EditRepoOption.  # noqa: E501

        either `true` to allow merging pull requests with a merge commit, or `false` to prevent merging pull requests with merge commits. `has_pull_requests` must be `true`.  # noqa: E501

        :return: The allow_merge_commits of this EditRepoOption.  # noqa: E501
        :rtype: bool
        """
        return self._allow_merge_commits

    @allow_merge_commits.setter
    def allow_merge_commits(self, allow_merge_commits):
        """Sets the allow_merge_commits of this EditRepoOption.

        either `true` to allow merging pull requests with a merge commit, or `false` to prevent merging pull requests with merge commits. `has_pull_requests` must be `true`.  # noqa: E501

        :param allow_merge_commits: The allow_merge_commits of this EditRepoOption.  # noqa: E501
        :type: bool
        """

        self._allow_merge_commits = allow_merge_commits

    @property
    def allow_rebase(self):
        """Gets the allow_rebase of this EditRepoOption.  # noqa: E501

        either `true` to allow rebase-merging pull requests, or `false` to prevent rebase-merging. `has_pull_requests` must be `true`.  # noqa: E501

        :return: The allow_rebase of this EditRepoOption.  # noqa: E501
        :rtype: bool
        """
        return self._allow_rebase

    @allow_rebase.setter
    def allow_rebase(self, allow_rebase):
        """Sets the allow_rebase of this EditRepoOption.

        either `true` to allow rebase-merging pull requests, or `false` to prevent rebase-merging. `has_pull_requests` must be `true`.  # noqa: E501

        :param allow_rebase: The allow_rebase of this EditRepoOption.  # noqa: E501
        :type: bool
        """

        self._allow_rebase = allow_rebase

    @property
    def allow_rebase_explicit(self):
        """Gets the allow_rebase_explicit of this EditRepoOption.  # noqa: E501

        either `true` to allow rebase with explicit merge commits (--no-ff), or `false` to prevent rebase with explicit merge commits. `has_pull_requests` must be `true`.  # noqa: E501

        :return: The allow_rebase_explicit of this EditRepoOption.  # noqa: E501
        :rtype: bool
        """
        return self._allow_rebase_explicit

    @allow_rebase_explicit.setter
    def allow_rebase_explicit(self, allow_rebase_explicit):
        """Sets the allow_rebase_explicit of this EditRepoOption.

        either `true` to allow rebase with explicit merge commits (--no-ff), or `false` to prevent rebase with explicit merge commits. `has_pull_requests` must be `true`.  # noqa: E501

        :param allow_rebase_explicit: The allow_rebase_explicit of this EditRepoOption.  # noqa: E501
        :type: bool
        """

        self._allow_rebase_explicit = allow_rebase_explicit

    @property
    def allow_squash_merge(self):
        """Gets the allow_squash_merge of this EditRepoOption.  # noqa: E501

        either `true` to allow squash-merging pull requests, or `false` to prevent squash-merging. `has_pull_requests` must be `true`.  # noqa: E501

        :return: The allow_squash_merge of this EditRepoOption.  # noqa: E501
        :rtype: bool
        """
        return self._allow_squash_merge

    @allow_squash_merge.setter
    def allow_squash_merge(self, allow_squash_merge):
        """Sets the allow_squash_merge of this EditRepoOption.

        either `true` to allow squash-merging pull requests, or `false` to prevent squash-merging. `has_pull_requests` must be `true`.  # noqa: E501

        :param allow_squash_merge: The allow_squash_merge of this EditRepoOption.  # noqa: E501
        :type: bool
        """

        self._allow_squash_merge = allow_squash_merge

    @property
    def archived(self):
        """Gets the archived of this EditRepoOption.  # noqa: E501

        set to `true` to archive this repository.  # noqa: E501

        :return: The archived of this EditRepoOption.  # noqa: E501
        :rtype: bool
        """
        return self._archived

    @archived.setter
    def archived(self, archived):
        """Sets the archived of this EditRepoOption.

        set to `true` to archive this repository.  # noqa: E501

        :param archived: The archived of this EditRepoOption.  # noqa: E501
        :type: bool
        """

        self._archived = archived

    @property
    def autodetect_manual_merge(self):
        """Gets the autodetect_manual_merge of this EditRepoOption.  # noqa: E501

        either `true` to enable AutodetectManualMerge, or `false` to prevent it. `has_pull_requests` must be `true`, Note: In some special cases, misjudgments can occur.  # noqa: E501

        :return: The autodetect_manual_merge of this EditRepoOption.  # noqa: E501
        :rtype: bool
        """
        return self._autodetect_manual_merge

    @autodetect_manual_merge.setter
    def autodetect_manual_merge(self, autodetect_manual_merge):
        """Sets the autodetect_manual_merge of this EditRepoOption.

        either `true` to enable AutodetectManualMerge, or `false` to prevent it. `has_pull_requests` must be `true`, Note: In some special cases, misjudgments can occur.  # noqa: E501

        :param autodetect_manual_merge: The autodetect_manual_merge of this EditRepoOption.  # noqa: E501
        :type: bool
        """

        self._autodetect_manual_merge = autodetect_manual_merge

    @property
    def default_branch(self):
        """Gets the default_branch of this EditRepoOption.  # noqa: E501

        sets the default branch for this repository.  # noqa: E501

        :return: The default_branch of this EditRepoOption.  # noqa: E501
        :rtype: str
        """
        return self._default_branch

    @default_branch.setter
    def default_branch(self, default_branch):
        """Sets the default_branch of this EditRepoOption.

        sets the default branch for this repository.  # noqa: E501

        :param default_branch: The default_branch of this EditRepoOption.  # noqa: E501
        :type: str
        """

        self._default_branch = default_branch

    @property
    def default_merge_style(self):
        """Gets the default_merge_style of this EditRepoOption.  # noqa: E501

        set to a merge style to be used by this repository: \"merge\", \"rebase\", \"rebase-merge\", or \"squash\". `has_pull_requests` must be `true`.  # noqa: E501

        :return: The default_merge_style of this EditRepoOption.  # noqa: E501
        :rtype: str
        """
        return self._default_merge_style

    @default_merge_style.setter
    def default_merge_style(self, default_merge_style):
        """Sets the default_merge_style of this EditRepoOption.

        set to a merge style to be used by this repository: \"merge\", \"rebase\", \"rebase-merge\", or \"squash\". `has_pull_requests` must be `true`.  # noqa: E501

        :param default_merge_style: The default_merge_style of this EditRepoOption.  # noqa: E501
        :type: str
        """

        self._default_merge_style = default_merge_style

    @property
    def description(self):
        """Gets the description of this EditRepoOption.  # noqa: E501

        a short description of the repository.  # noqa: E501

        :return: The description of this EditRepoOption.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this EditRepoOption.

        a short description of the repository.  # noqa: E501

        :param description: The description of this EditRepoOption.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def external_tracker(self):
        """Gets the external_tracker of this EditRepoOption.  # noqa: E501


        :return: The external_tracker of this EditRepoOption.  # noqa: E501
        :rtype: ExternalTracker
        """
        return self._external_tracker

    @external_tracker.setter
    def external_tracker(self, external_tracker):
        """Sets the external_tracker of this EditRepoOption.


        :param external_tracker: The external_tracker of this EditRepoOption.  # noqa: E501
        :type: ExternalTracker
        """

        self._external_tracker = external_tracker

    @property
    def external_wiki(self):
        """Gets the external_wiki of this EditRepoOption.  # noqa: E501


        :return: The external_wiki of this EditRepoOption.  # noqa: E501
        :rtype: ExternalWiki
        """
        return self._external_wiki

    @external_wiki.setter
    def external_wiki(self, external_wiki):
        """Sets the external_wiki of this EditRepoOption.


        :param external_wiki: The external_wiki of this EditRepoOption.  # noqa: E501
        :type: ExternalWiki
        """

        self._external_wiki = external_wiki

    @property
    def has_issues(self):
        """Gets the has_issues of this EditRepoOption.  # noqa: E501

        either `true` to enable issues for this repository or `false` to disable them.  # noqa: E501

        :return: The has_issues of this EditRepoOption.  # noqa: E501
        :rtype: bool
        """
        return self._has_issues

    @has_issues.setter
    def has_issues(self, has_issues):
        """Sets the has_issues of this EditRepoOption.

        either `true` to enable issues for this repository or `false` to disable them.  # noqa: E501

        :param has_issues: The has_issues of this EditRepoOption.  # noqa: E501
        :type: bool
        """

        self._has_issues = has_issues

    @property
    def has_projects(self):
        """Gets the has_projects of this EditRepoOption.  # noqa: E501

        either `true` to enable project unit, or `false` to disable them.  # noqa: E501

        :return: The has_projects of this EditRepoOption.  # noqa: E501
        :rtype: bool
        """
        return self._has_projects

    @has_projects.setter
    def has_projects(self, has_projects):
        """Sets the has_projects of this EditRepoOption.

        either `true` to enable project unit, or `false` to disable them.  # noqa: E501

        :param has_projects: The has_projects of this EditRepoOption.  # noqa: E501
        :type: bool
        """

        self._has_projects = has_projects

    @property
    def has_pull_requests(self):
        """Gets the has_pull_requests of this EditRepoOption.  # noqa: E501

        either `true` to allow pull requests, or `false` to prevent pull request.  # noqa: E501

        :return: The has_pull_requests of this EditRepoOption.  # noqa: E501
        :rtype: bool
        """
        return self._has_pull_requests

    @has_pull_requests.setter
    def has_pull_requests(self, has_pull_requests):
        """Sets the has_pull_requests of this EditRepoOption.

        either `true` to allow pull requests, or `false` to prevent pull request.  # noqa: E501

        :param has_pull_requests: The has_pull_requests of this EditRepoOption.  # noqa: E501
        :type: bool
        """

        self._has_pull_requests = has_pull_requests

    @property
    def has_wiki(self):
        """Gets the has_wiki of this EditRepoOption.  # noqa: E501

        either `true` to enable the wiki for this repository or `false` to disable it.  # noqa: E501

        :return: The has_wiki of this EditRepoOption.  # noqa: E501
        :rtype: bool
        """
        return self._has_wiki

    @has_wiki.setter
    def has_wiki(self, has_wiki):
        """Sets the has_wiki of this EditRepoOption.

        either `true` to enable the wiki for this repository or `false` to disable it.  # noqa: E501

        :param has_wiki: The has_wiki of this EditRepoOption.  # noqa: E501
        :type: bool
        """

        self._has_wiki = has_wiki

    @property
    def ignore_whitespace_conflicts(self):
        """Gets the ignore_whitespace_conflicts of this EditRepoOption.  # noqa: E501

        either `true` to ignore whitespace for conflicts, or `false` to not ignore whitespace. `has_pull_requests` must be `true`.  # noqa: E501

        :return: The ignore_whitespace_conflicts of this EditRepoOption.  # noqa: E501
        :rtype: bool
        """
        return self._ignore_whitespace_conflicts

    @ignore_whitespace_conflicts.setter
    def ignore_whitespace_conflicts(self, ignore_whitespace_conflicts):
        """Sets the ignore_whitespace_conflicts of this EditRepoOption.

        either `true` to ignore whitespace for conflicts, or `false` to not ignore whitespace. `has_pull_requests` must be `true`.  # noqa: E501

        :param ignore_whitespace_conflicts: The ignore_whitespace_conflicts of this EditRepoOption.  # noqa: E501
        :type: bool
        """

        self._ignore_whitespace_conflicts = ignore_whitespace_conflicts

    @property
    def internal_tracker(self):
        """Gets the internal_tracker of this EditRepoOption.  # noqa: E501


        :return: The internal_tracker of this EditRepoOption.  # noqa: E501
        :rtype: InternalTracker
        """
        return self._internal_tracker

    @internal_tracker.setter
    def internal_tracker(self, internal_tracker):
        """Sets the internal_tracker of this EditRepoOption.


        :param internal_tracker: The internal_tracker of this EditRepoOption.  # noqa: E501
        :type: InternalTracker
        """

        self._internal_tracker = internal_tracker

    @property
    def mirror_interval(self):
        """Gets the mirror_interval of this EditRepoOption.  # noqa: E501

        set to a string like `8h30m0s` to set the mirror interval time  # noqa: E501

        :return: The mirror_interval of this EditRepoOption.  # noqa: E501
        :rtype: str
        """
        return self._mirror_interval

    @mirror_interval.setter
    def mirror_interval(self, mirror_interval):
        """Sets the mirror_interval of this EditRepoOption.

        set to a string like `8h30m0s` to set the mirror interval time  # noqa: E501

        :param mirror_interval: The mirror_interval of this EditRepoOption.  # noqa: E501
        :type: str
        """

        self._mirror_interval = mirror_interval

    @property
    def name(self):
        """Gets the name of this EditRepoOption.  # noqa: E501

        name of the repository  # noqa: E501

        :return: The name of this EditRepoOption.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this EditRepoOption.

        name of the repository  # noqa: E501

        :param name: The name of this EditRepoOption.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def private(self):
        """Gets the private of this EditRepoOption.  # noqa: E501

        either `true` to make the repository private or `false` to make it public. Note: you will get a 422 error if the organization restricts changing repository visibility to organization owners and a non-owner tries to change the value of private.  # noqa: E501

        :return: The private of this EditRepoOption.  # noqa: E501
        :rtype: bool
        """
        return self._private

    @private.setter
    def private(self, private):
        """Sets the private of this EditRepoOption.

        either `true` to make the repository private or `false` to make it public. Note: you will get a 422 error if the organization restricts changing repository visibility to organization owners and a non-owner tries to change the value of private.  # noqa: E501

        :param private: The private of this EditRepoOption.  # noqa: E501
        :type: bool
        """

        self._private = private

    @property
    def template(self):
        """Gets the template of this EditRepoOption.  # noqa: E501

        either `true` to make this repository a template or `false` to make it a normal repository  # noqa: E501

        :return: The template of this EditRepoOption.  # noqa: E501
        :rtype: bool
        """
        return self._template

    @template.setter
    def template(self, template):
        """Sets the template of this EditRepoOption.

        either `true` to make this repository a template or `false` to make it a normal repository  # noqa: E501

        :param template: The template of this EditRepoOption.  # noqa: E501
        :type: bool
        """

        self._template = template

    @property
    def website(self):
        """Gets the website of this EditRepoOption.  # noqa: E501

        a URL with more information about the repository.  # noqa: E501

        :return: The website of this EditRepoOption.  # noqa: E501
        :rtype: str
        """
        return self._website

    @website.setter
    def website(self, website):
        """Sets the website of this EditRepoOption.

        a URL with more information about the repository.  # noqa: E501

        :param website: The website of this EditRepoOption.  # noqa: E501
        :type: str
        """

        self._website = website

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(EditRepoOption, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, EditRepoOption):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, EditRepoOption):
            return True

        return self.to_dict() != other.to_dict()
