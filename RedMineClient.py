import requests


class RedMineClient:
    def __init__(self, serverurl, apikey):
        self.server_url = serverurl
        self.api_key = apikey
        self.issue_path = "/issues/{0}.json"
        self.time_entry_path = "/time_entries.json"
        self.activity_endpoint = "/enumerations/time_entry_activities.json"

    def get_issue(self, issueid):
        headers = {'content-type': 'application/json', 'X-Redmine-API-Key': self.api_key}
        return requests.get(self.server_url + self.issue_path.format(issueid), headers=headers)





