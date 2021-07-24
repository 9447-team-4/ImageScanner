import argparse
from Reporters import *
from StaticPRReporter import SonarPRReporter
from FuzzReporter import ZAPPRReporter
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    parser = argparse.ArgumentParser('gitea-reporter')
    subparsers = parser.add_subparsers(dest='type')
    parser_pr = subparsers.add_parser('pr', help="Report pull request results")

    subparsers_pr = parser_pr.add_subparsers(dest ='tool', help='The tool to report')
    parser_image = subparsers_pr.add_parser('image-scan')
    parser_image.add_argument('branch-image', help='The branch or image to compare against')
    parser_static = subparsers_pr.add_parser('static')
    parser_dynamic = subparsers_pr.add_parser('dynamic')
    parser_image.add_argument('pr_id', help='The pull request id number')
    parser_static.add_argument('pr_id', help='The pull request id number')
    parser_dynamic.add_argument('pr_id', help='The pull request id number')

    parser_main = subparsers.add_parser('main', help="Scan a main branch's Dockerfile for vulnerabilities")
    parser_main.add_argument('image-scan', help="Image scan tool to use")
    parser_main.add_argument('branch-image', help='The branch or image you want to scan')

    args = parser.parse_args()

    if args.type == 'pr':
        gitea = GiteaService(os.getenv('GITEA_REPO'), os.getenv('GITEA_USERNAME'), os.getenv('GITEA_TOKEN'),
                             os.getenv('GITEA_HOST'), os.getenv('GITEA_PORT'))
        if args.tool == "image-scan":
            # TODO
            # call image scan
            pass
        elif args.tool == "static":
            sonar = SonarPRReporter(gitea, args.pr_id)
            sonar.process_pull_review()
            sonar.commit_review()
        elif args.tool == "dynamic":
            zap = ZAPPRReporter(gitea, args.pr_id)
            zap.process_pull_review()
            zap.commit_review()
    elif args.type == 'main':
        # TODO
        # Scan branch or image against main
        pass
