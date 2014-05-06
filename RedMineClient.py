import requests
import json


class TimeEntryRequest(object):
    def __init__(self, time_entry):
        self.time_entry = time_entry


class TimeEntry(object):
    def __init__(self, activity_id, issue_id, comments, hours):
        self.hours = hours
        self.comments = comments
        self.issue_id = issue_id
        self.activity_id = activity_id


class RedMineClient:
    def __init__(self, serverurl, apikey):
        self.server_url = serverurl
        self.api_key = apikey
        self.issue_path = "/issues/{0}.json"
        self.time_entry_path = "/time_entries.json"
        self.activity_endpoint = "/enumerations/time_entry_activities.json"
        self.headers = {'content-type': 'application/json', 'X-Redmine-API-Key': self.api_key}


    def get_issue(self, issueid):
        try:
            issue = requests.get(self.server_url + self.issue_path.format(issueid), headers=self.headers).json()
            return issue["issue"]
        except ValueError:
            issue = None
        return issue

    def get_activities(self):
        try:
            activities = requests.get(self.server_url + self.activity_endpoint, headers=self.headers).json()
            return activities["time_entry_activities"]
        except ValueError:
            activities = None
        return activities

    def post_time_entry(self, time_entry_request):
        inputData=json.dumps(time_entry_request, default=lambda o: o.__dict__)
        r = requests.post(self.server_url + self.time_entry_path, data=inputData, headers=self.headers)
        return r.status_code == 201





