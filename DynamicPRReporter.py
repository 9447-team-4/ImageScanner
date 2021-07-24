from Reporters import PullRequestReporter, GitService
import boto3
import os
import json


class ZAPPRReporter(PullRequestReporter):

    def __init__(self, git_service: GitService, pr_id: int):
        super(ZAPPRReporter, self).__init__(git_service, pr_id)
        self._bucket_name = os.getenv('S3_BUCKET_NAME')
        self._s3_client = boto3.client('s3')
        self._s3_bucket = boto3.resource('s3')

    def _get_report(self):
        report_url = self._s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self._bucket_name, 'Key': 'report.html'},
            ExpiresIn=86400)

        return report_url

    def _get_metrics(self):
        obj = self._s3_bucket.Object('soteriafuzzreport', 'report.json')
        json_obj = json.loads(obj.get()['Body'].read().decode('utf-8'))
        alerts = {'0': 0, '1': 0, '2': 0, '3': 0}

        for site in json_obj['site']:
            for alert in site['alerts']:
                alerts[alert['riskcode']] += 1

        return alerts

    def _create_message(self):
        alerts = self._get_metrics()
        msg = "--- OWASP ZAP fuzzing results ---\n" \
              "High: {}\n" \
              "Medium: {}\n" \
              "Low: {}\n" \
              "Informational: {}\n\n".format(alerts['3'], alerts['2'], alerts['1'], alerts['0'])
        report_url = self._get_report()
        msg += f"View more results: {report_url}"

        return msg

    def process_pull_review(self):
        msg = self._create_message()
        self.pull_review.body = msg
