#!/usr/bin/env python3

import sys
import os
import argparse
import json
from git import Repo
from functools import reduce

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


class Vulnerability(object):
    def __init__(self, id='', title='', cvssScore='', patches=[]):
        self.id = id
        self.title = title
        self.cvssScore = cvssScore
        self.patches = patches

def open_repo(repopath):
    return Repo(repopath)


def diff_reports(*reports):
    """
        Check if the reports have different vulnerabilities,
        Returns a set of all vulnerabilities that do not exist in all reports

    """
    from itertools import groupby

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
        print(bcolors.OKGREEN + 'Building the image on branch ' + bcolors.WARNING + branch  + bcolors.ENDC + '...')
        os.system(f'docker build -t image-scan -f {dockerfile} {repopath} > /dev/null')
        print(bcolors.OKGREEN + 'Scanning image on branch ' + bcolors.WARNING + branch  + bcolors.ENDC + '...')
        json_out = os.popen(f"docker scan --json --group-issues --file {dockerfile} image-scan").read()
        yield json.loads(json_out)

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def submitIssue(vuln, target):
    """
    Send an api request to target to submit an issue for the vulnerability
    """
    pass


def scan(repopath, severity, branch):
    """
        Scan a repo's dockerfile for any vulnerabilities.

        returns: a list of vulnerabilities 
    """

    repo = open_repo(repopath)

    json_result = next(scan_branches(repo, branch))
    
    fil = lambda x: x['severity'] == severity
    
    vuln_list = list(filter(fil, json_result['vulnerabilities']))
    
    return vuln_list

def compare(repopath, severity, target, base):
    """
        Returns a true if the base introduces some new
        vulnerabilities into target. 
    """
    repo = open_repo(repopath)
    
    # this returns a list of vulnerabilities that does not exist in
    # the branch itself. So the ideal case is that both list of 
    # vulnerabilities are the same, which means the base branch
    # is not introducing any new vulnerabilities 
    report_target, report_base = scan_branches(repo, target, base)
       
    fil = lambda x: x['severity'] == severity
    
    report_target['vulnerabilities'] = list(filter(fil, report_target['vulnerabilities']))
    report_base['vulnerabilities'] = list(filter(fil, report_base['vulnerabilities']))
    [diff_vulns_target, diff_vulns_base] = diff_reports(report_target, report_base)
    
    if diff_vulns_target:
        print(bcolors.FAIL + f'Branch {base} is introducing new vulnerabilities to branch {target}!')
        print(f'Vulnerabilities found: {diff_vulns_target}' + bcolors.ENDC)
    
        return True
    
    print(bcolors.OKGREEN + 'No new vulnerabilities detected' + bcolors.ENDC)
    return False

if __name__=="__main__":
    
    parser = argparse.ArgumentParser('image-scan')
    
    subparsers = parser.add_subparsers(dest='subcommand')
    
    parser_scan = subparsers.add_parser('scan', help="Scan a branch's Dockerfile for vulnerabilities")

    parser_scan.add_argument(
            '--severity', 
            nargs=1, default='low', 
            choices=['low', 'medium', 'high'],
            help='The lowest severity you want to detect')

    parser_scan.add_argument('branch', help='The branch you want to scan')
    parser_scan.add_argument('--issue_uri', help='The uri to send a the vulnerability to.')

    parser_compare = subparsers.add_parser('compare', help="Compare two branches for vulnerabilities")
    
    parser_compare.add_argument(
            '--severity',
            nargs=1, default='low',
            choices=['low', 'medium', 'high'],
            help='The lowest severity you want to consider while comparing')

    parser_compare.add_argument(
            '--branches',
            nargs=2,
            metavar=('TARGET', 'BASE'),
            help='The branches you want to compare.')

    parser.add_argument('repo', type=dir_path,help='The path to the repo that contains a Dockerfile')
    
    args = parser.parse_args()
    
    if args.subcommand == 'scan':
        vulns = scan(args.repo, *args.severity, args.branch)
        
        if vulns:
            if args.issue_uri:
                submitIssue(vulns, args.issue_uri)
            exit(1)

    elif args.subcommand == 'compare':
        result = compare(args.repo, *args.severity, *args.branches)
        if result:
            exit(1)




