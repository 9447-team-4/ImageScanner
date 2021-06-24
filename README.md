# ImageScanner
A tool to scan images which features git. Allows scanning branches and comparing between them.

## Overview
The tool provides the ability to scan a Dockerfile that exists in a branch in a repo. It also allows you to compare two different Dockerfiles that exist in two different branches  for the purposes 
of validating whether a branch in a pull request is introducing new vulnerabilities. The tool uses Snyk.io and docker scan plugin so you are required to have it installed and authorized.
