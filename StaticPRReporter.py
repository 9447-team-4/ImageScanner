import os
from sonarqube import SonarQubeClient
from Reporters import GitService, PullRequestReporter


class SonarPRReporter(PullRequestReporter):

    def __init__(self, git_service: GitService, pr_id: int):
        super(SonarPRReporter, self).__init__(git_service, pr_id)
        self._exit_status = 0
        self._sonar_url = os.getenv('SONAR_URL')
        self._sonar_login = os.getenv('SONAR_LOGIN')
        self._sonar_password = os.getenv('SONAR_PASSWORD')
        self._sonar_key = os.getenv('SONAR_KEY')
        self._sonar = SonarQubeClient(sonarqube_url=self._sonar_url, username=self._sonar_login,
                                      password=self._sonar_password)

    @property
    def exit_status(self):
        return self._exit_status

    def _check_files(self):
        if not os.path.exists('sonar-project.properties'):
            raise Exception("sonar-project.properties file not found")
        return True

    def _get_project(self):
        projects = list(self._sonar.projects.search_projects())
        for p in projects:
            if p['key'] == self._sonar_key:
                return p
        raise Exception("No SonarQube project found with given key")

    def _get_sonar_metrics(self):
        project_data = self._get_project()
        msg = ""
        quality_gate = self._sonar.qualitygates.get_project_qualitygates_status(projectKey=self._sonar_key)
        msg += f"Project state: {quality_gate['projectStatus']['status']}\n"
        if quality_gate['projectStatus']['status'] == "ERROR":
            self._exit_status = 1
        component = self._sonar.measures.get_component_with_specified_measures(component=project_data['key'],
                                                                               fields="metrics, periods",
                                                                               metricKeys="code_smells, bugs, "
                                                                                          "vulnerabilities")
        project = {'name': component['component']['name']}
        msg += "| Risk Level\t\t | Amount of Vulnerabilities |\n" \
               "| -------------- | ------------------------- |\n"
        for measure in component['component']['measures']:
            project[measure['metric']] = measure['value']
            msg += f"| {measure['metric'].capitalize()}\t\t | {project[measure['metric']]} |\n"
        return msg

    def _create_message(self):
        msg = "# SonarQube Results\n"
        msg += self._get_sonar_metrics()
        url = f"{self._sonar_url}/dashboard?id={self._sonar_key}"
        msg += f"\nView more details on: {url}\n"
        return msg

    def process_pull_review(self):
        msg = self._create_message()
        self.pull_review.body = msg
