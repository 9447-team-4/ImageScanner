from Reporters import PullRequestReporter, GitService
import boto3
import os
import json


class ZAPPRReporter(PullRequestReporter):

    def __init__(self, git_service: GitService, pr_id: int):
        super(ZAPPRReporter, self).__init__(git_service, pr_id)
        self._exit_status = 0
        self._bucket_name = os.getenv('S3_BUCKET_NAME')
        self._s3_client = boto3.client('s3')
        self._s3_bucket = boto3.resource('s3')

    @property
    def exit_status(self):
        return self._exit_status

    def _get_report(self):
        report_url = self._s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self._bucket_name, 'Key': 'report.html'},
            ExpiresIn=86400)

        return report_url

    def _get_metrics(self):
        obj = self._s3_bucket.Object(self._bucket_name, 'report.json')
        json_obj = json.loads(obj.get()['Body'].read().decode('utf-8'))
        alerts = {'0': 0, '1': 0, '2': 0, '3': 0}

        for site in json_obj['site']:
            for alert in site['alerts']:
                alerts[alert['riskcode']] += 1

        # If high risk vuln > 0
        if alerts['3'] > 0:
            self._exit_status = 1

        return alerts

    def _create_message(self):
        alerts = self._get_metrics()
        msg = "# OWASP ZAP Fuzzing Results\n" \
              "| Risk Level     | Amount of Vulnerabilities |\n" \
              "| -------------- | ------------------------- |\n" \
             f"| High           | {alerts['3']}             |\n" \
             f"| Medium         | {alerts['2']}             |\n" \
             f"| Low            | {alerts['1']}             |\n" \
             f"| Informational  | {alerts['0']}             |\n\n"

        report_url = self._get_report()
        msg += f"View more results:\n{report_url}"

        return msg

    def process_pull_review(self):
        msg = self._create_message()
        self.pull_review.body = msg
