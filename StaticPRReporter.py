import os
from sonarqube import SonarQubeClient
from Reporters import *
from dotenv import load_dotenv

load_dotenv()


class SonarPRReporter(PullRequestReporter):

    def __init__(self, git_service: GitService, pr_id: int):
        super(SonarPRReporter, self).__init__(git_service, pr_id)
        # self.check_files()
        self._sonar_url = os.getenv('SONAR_URL')
        self._sonar_login = os.getenv('SONAR_LOGIN')
        self._sonar_password = os.getenv('SONAR_PASSWORD')
        self._sonar_key = os.getenv('SONAR_KEY')
        self._sonar = SonarQubeClient(sonarqube_url=self._sonar_url, username=self._sonar_login,
                                      password=self._sonar_password)

    def check_files(self):
        if not os.path.exists('sonar-project.properties'):
            raise Exception("sonar-project.properties file not found")
        return True

    def get_project(self):
        projects = list(self._sonar.projects.search_projects())
        for p in projects:
            if p['key'] == self._sonar_key:
                return p
        raise Exception("No SonarQube project found with given key")

    def get_sonar_metrics(self):
        project_data = self.get_project()
        msg = ""
        quality_gate = self._sonar.qualitygates.get_project_qualitygates_status(projectKey=self._sonar_key)
        msg += f"Project state: {quality_gate['projectStatus']['status']}\n"
        component = self._sonar.measures.get_component_with_specified_measures(component=project_data['key'],
                                                                               fields="metrics, periods",
                                                                               metricKeys="code_smells, bugs, "
                                                                                          "vulnerabilities")
        project = {'name': component['component']['name']}
        for measure in component['component']['measures']:
            project[measure['metric']] = measure['value']
            msg += f"\t{measure['metric']}: {project[measure['metric']]}\n"
        return msg

    def create_message(self):
        msg = "Current project SonarQube scan results\n"
        msg += self.get_sonar_metrics()
        url = f"{self._sonar_url}/dashboard?id={self._sonar_key}"
        msg += f"View more details on: {url}\n"
        return msg

    def process_pull_review(self):
        msg = self.create_message()
        self.pull_review.body = msg

