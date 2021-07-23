import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser('gitea-reporter')

    subparsers = parser.add_subparsers(dest='type')

    parser_pr = subparsers.add_parser('pr', help="Report pull request results")

    parser_main = subparsers.add_parser('main', help="Scan a main branch's Dockerfile for vulnerabilities")

    subparsers_pr = parser_pr.add_subparsers(dest ='tool', help='The tool to report')

    parser_image = subparsers_pr.add_parser('image-scan')

    parser_image.add_argument('branch-image', help='The branch or image to compare against')

    parser_static = subparsers_pr.add_parser('static')

    parser_dynamic = subparsers_pr.add_parser('dynamic')

    parser_image.add_argument('pr_id', help='The pull request id number')
    parser_static.add_argument('pr_id', help='The pull request id number')
    parser_dynamic.add_argument('pr_id', help='The pull request id number')

    parser_main.add_argument('image-scan', help="Image scan tool to use")
    parser_main.add_argument('branch-image', help='The branch or image you want to scan')

    args = parser.parse_args()

    if args.type == 'pr':
        if args.tool == "image-scan":
            # call image scan
            pass
        elif args.tool == "static":
            # create static reporter
            pass
        elif args.tool == "dynamic":
            # create dynamic reporter
            pass
    elif args.type == 'main':
        pass
