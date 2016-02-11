import json

import requests


class TimeEntryRequest(object):

    def __init__(self, time_entry):
        self.time_entry = time_entry


class TimeEntry(object):

    def __init__(self, activity_id, issue_id, comments, time_in_minutes):
        self.hours = time_in_minutes+"m"
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
        self.headers = {
            'content-type': 'application/json',
            'X-Redmine-API-Key': self.api_key
        }
        self.proxies = {
            "http": "http://localhost:3128",
            "https": "https://localhost:3128",
        }

    def get_issue(self, issueid):
        try:
            issue = requests.get(
                self.server_url + self.issue_path.format(issueid),
                headers=self.headers, verify=False,
                ).json()
                # proxies=self.proxies).json()
            return issue["issue"]
        except ValueError:
            issue = False
            return issue
        return issue

    def getActivities(self):
        try:
            activities = requests.get(
                self.server_url + self.activity_endpoint, headers=self.headers,
                verify=False
            ).json()
            # , proxies=self.proxies).json()
            return activities["time_entry_activities"]
        except ValueError:
            activities = None
        return activities

    def post_time_entry(self, time_entry):
        time_entry_request = TimeEntryRequest(time_entry)
        inputData = json.dumps(
            time_entry_request, default=lambda o: o.__dict__)
        r = requests.post(self.server_url + self.time_entry_path,
                          data=inputData, headers=self.headers, verify=False)
        return r.status_code == 201
