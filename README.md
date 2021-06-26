# ImageScanner

A tool to scan images which features git. Allows scanning branches and comparing between them.

## Overview

The tool provides the ability to scan a Dockerfile that exists in a branch in a repo. It also allows you to compare two different Dockerfiles that exist in two different branches for the purposes
of validating whether a branch in a pull request is introducing new vulnerabilities. The tool uses Snyk.io and docker scan plugin so you are required to have it installed and authorized.

## Setup

### Requirements

- python v3.7 or higher
- pip

### Installing the required dependencies

To install the dependencies you need to run the following:

```bash
$ pip install -r requirements.txt
```

To run the program. You need to first define a .env file that has the following:

```.env
GITEA_TOKEN=YOUR-ACCESS-TOKEN
GITEA_USERNAME=USERNAME-TO-ACCESS-GITEA-AS
GITEA_HOST=localhost
GITEA_PORT=3000
GITEA_REPO=YOUR-CODE-REPO
```

an example .env.example is provided in the repo as well.

### Running the program

To scan a target branch given the path to the repo (which contains the Dockerfile at the root) and a target branch, do the following:

```bash
$ ./image-scan.py scan [-h] [--severity {low,medium,high}]
                       [--git_service {github,bitbucket,gitlab,gitea}]
                       <branch> <repo-path>

# Example
$ ./image-scan.py scan master . # this scans the current image-scan directory's Dockerfile (Assuming it exists on Gitea at the moment)
```

Here, the following arguments are:

```bash
positional arguments:
  branch                The branch you want to scan

optional arguments:
  -h, --help            show this help message and exit
  --severity {low,medium,high}
                        The lowest severity you want to detect
  --git_service {github,bitbucket,gitlab,gitea}
                        The git service you to want to report the
                        vulnerability to.
```

Currently, only gitea is supported as a reporting service.

To compare branches:

```bash
$ ./image-scan.py compare [-h] [--severity {low,medium,high}]
                       [--git_service {github,bitbucket,gitlab,gitea}]
                       <target_branch> <base_branch> <repo-path>

# Example
$ ./image-scan.py compare master feature . # check whether feature is introducing vulnerabilites to master in this repo (triggered by a pull request for example)

```

Here the arguments are:

```bash
positional arguments:
  target_branch         The target branch you want in to compare with.
  base_branch           The base branch you want to compare with.
  repo_path             The path to the repo
optional arguments:
  -h, --help            show this help message and exit
  --severity {low,medium,high}
                        The lowest severity you want to consider while
                        comparing
```

Happy coding!
