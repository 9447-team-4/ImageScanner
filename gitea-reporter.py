#!/usr/bin/env python3

import argparse
from Reporters import GiteaService
from StaticPRReporter import SonarPRReporter
from DynamicPRReporter import ZAPPRReporter
from ImageReporters import ImagePRReporter, ImageIssueReporter, Severity
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    parser = argparse.ArgumentParser('gitea-reporter')
    subparsers = parser.add_subparsers(dest='type')
    subparsers.required = True

    parser_pr = subparsers.add_parser('pr', help="Report results via pull request review")

    subparsers_pr = parser_pr.add_subparsers(dest='stage', help='The pipeline stage to report')
    subparsers_pr.required = True

    parser_static = subparsers_pr.add_parser('static')
    parser_pr_image = subparsers_pr.add_parser('image-scan')
    parser_dynamic = subparsers_pr.add_parser('dynamic')

    parser_pr_image.add_argument('base', help='The image that is initiated from the PR (feature branch)')
    parser_pr_image.add_argument('target', help='The image that currently exists in the target branch (main '
                                                'branch)')
    parser_pr_image.add_argument('--severity-threshold', nargs=1, default='low',
                                 choices=['low', 'medium', 'high', 'critical'])
    parser_pr_image.add_argument('pr_id', help='The pull request id number')

    parser_dynamic.add_argument('pr_id', help='The pull request id number')
    parser_static.add_argument('pr_id', help='The pull request id number')

    parser_issue = subparsers.add_parser('issue', help="Report pipeline stage via issues.")

    subparsers_issue = parser_issue.add_subparsers(dest='stage', help='Stage of pipeline to report as issues')
    subparsers_issue.required = True
    parser_issue_image = subparsers_issue.add_parser('image-scan')

    parser_issue_image.add_argument('image', help='The image that needs to be scanned.')
    parser_issue_image.add_argument('--severity-threshold', nargs=1, default='low',
                                    choices=['low', 'medium', 'high', 'critical'])

    args = parser.parse_args()

    gitea = GiteaService(os.getenv('GITEA_REPO'), os.getenv('GITEA_USERNAME'), os.getenv('GITEA_TOKEN'),
                         os.getenv('GITEA_HOST'), os.getenv('GITEA_PORT'))

    if args.type == 'pr':

        pr_reporter = None
        if args.stage == "image-scan":
            pr_reporter = ImagePRReporter(gitea, args.pr_id, os.getenv('SNYK_TOKEN'), args.base, \
                                          args.target, Severity[args.severity_threshold])

        elif args.stage == "static":
            pr_reporter = SonarPRReporter(gitea, args.pr_id)
        elif args.stage == "dynamic":
            pr_reporter = ZAPPRReporter(gitea, args.pr_id)

        pr_reporter.process_pull_review()
        pr_reporter.commit_review()

        if isinstance(pr_reporter, ImagePRReporter) or isinstance(pr_reporter, SonarPRReporter):
            exit(pr_reporter.exit_status)

    elif args.type == 'issue':
        issue_reporter = ImageIssueReporter(gitea, os.getenv('SNYK_TOKEN'), args.image, \
                                            Severity[args.severity_threshold])

        issue_reporter.process_issues()
        issue_reporter.commit_issues()
