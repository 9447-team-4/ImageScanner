from Reporters import *
import boto3
import os
import json
from dotenv import load_dotenv

load_dotenv()


class ZAPPRReporter(PullRequestReporter):

    def __init__(self, git_service: GitService, pr_id: int):
        super(ZAPPRReporter, self).__init__(git_service, pr_id)
        self._bucket_name = os.getenv('S3_BUCKET_NAME')
        self._s3_client = boto3.client('s3')
        self._s3_bucket = boto3.resource('s3')

    def get_report(self):
        report_url = self._s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self._bucket_name, 'Key': 'report.html'},
            ExpiresIn=300)

        return report_url

    def get_metrics(self):
        obj = self._s3_bucket.Object('soteriafuzzreport', 'report.json')
        json_obj = json.loads(obj.get()['Body'].read().decode('utf-8'))
        alerts = {'0': 0, '1': 0, '2': 0, '3': 0}

        for site in json_obj['site']:
            for alert in site['alerts']:
                alerts[alert['riskcode']] += 1

        return alerts

    def create_message(self):
        alerts = self.get_metrics()
        msg = "--- OWASP ZAP fuzzing results ---\n" \
              "High: {}\n" \
              "Medium: {}\n" \
              "Low: {}\n" \
              "Informational: {}\n\n".format(alerts['3'], alerts['2'], alerts['1'], alerts['0'])
        report_url = self.get_report()
        msg += f"View more results: {report_url}"

        return msg

    def process_pull_review(self):
        msg = self.create_message()
        self.pull_review.body = msg


giteatest = GiteaService(os.getenv('GITEA_REPO'), os.getenv('GITEA_USERNAME'), os.getenv('GITEA_TOKEN'),
                         os.getenv('GITEA_HOST'), os.getenv('GITEA_PORT'))

zap = ZAPPRReporter(giteatest, 1)
zap.process_pull_review()
zap.commit_review()
