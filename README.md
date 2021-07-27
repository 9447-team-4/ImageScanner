# Gitea Reporter

## Overview

This tool provides a method for tools within the pipeline to report back to the Gitea through the use of issues and pull request comments.

## Setup

### Requirements

- python v3.7 or higher
- pip
- Snyk CLI
	- Instructions guide: https://support.snyk.io/hc/en-us/articles/360003812538-Install-the-Snyk-CLI

### Installing the required dependencies

Begin by first cloning the repository:

```bash
$ git clone https://github.com/9447-team-4/ImageScanner.git
```

To install the dependencies, you need to run the following:

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
SONAR_URL=YOUR-SONAR-URL
SONAR_LOGIN=YOUR-SONAR-USERNAME-OR-TOKEN
SONAR_PASSWORD=YOUR-SONAR-PASSWORD-BLANK-IF-TOKEN
SONAR_KEY=YOUR-SONAR-PROJECT-KEY
S3_BUCKET_NAME=YOUR-S3-BUCKET-NAME
SNYK_TOKEN=YOUR-SNYK-TOKEN
```

an example .env.example is provided in the repo as well.

---

### Setting up S3 bucket with AWS

Log into your IAM Console on AWS, then navigate

`Account name @ ID > My Security Credentials > Access keys for CLI, SDK, & API access > Create access key`

With the access ID and generated secret access key, enter the credentials in the following files

Create a file `~/.aws/credentials` with

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

Create a file `~/.aws/config` with

```
[default]
region=YOUR_REGION
```

Alternatively, you can change these files through the AWS CLI

To install the CLI, run the commands

```
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Then configure files by using

```
aws configure
```

---

### Running the program

This tool provides 2 functionalities one dealing with pull requests and one dealing with the issues.

To report to a specific pull request with the results of a tool:

```bash
# Pull request reporter (static/dynamic)
$ ./gitea-reporter.py pr {static,dynamic} pr_id

# Example
$ ./gitea-reporter.py pr static 1 # This will comment the results of static analysis on pull request id 1

# Pull request reporter (image-scan)
$ ./gitea-reporter.py pr image-scan [--severity-threshold {low,medium,high,critical}] base target pr_id
```

To report to the issues with the results of a tool:

```bash
# Issue reporter
$ ./gitea-reporter.py issue image-scan [--severity-threshold {low,medium,high,critical}] image

# Example
$ ./gitea-reporter.py issue image-scan --severity-threshold=critical image # This will create an issue detailing the issues of critical severity
```

### Alternative method: Installing and Running the program

Soterias gitea reporter is also available as a Docker image and can be used as follows:

```bash
docker run --env-file {path-to-env-file} soterias/gitea-reporter {arguments}
```

Where the env file will contain all the required variables as specified above.
Refer to Running the program section for list of arguments to provide.

:) :D
