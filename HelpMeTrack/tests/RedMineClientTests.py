import unittest

from RedMineClient import *


class RedMineClientTests(unittest.TestCase):
    def setUp(self):
        self.client = RedMineClient("https://support.targetintegration.com", "c3a7f2f4562ed90ff5bc9b6d9e0574f4d434d54e")
        pass

    def test_getIssue(self):
        print(" Trying to get Issue")
        issue = self.client.get_issue(1)
        self.assertIsNotNone(issue)
        print(issue)
        print(issue["subject"])

    def test_getIssue_NotFound(self):
        print("Issue that is not found")
        issue = self.client.get_issue(846548768)
        self.assertIsNone(issue)
        print(" issue not found ")


    def test_getActivites(self):
        print("trying to get activities")
        activities = self.client.get_activities()
        self.assertIsNotNone(activities)
        print(list(map(lambda x: x["name"].encode('ascii', 'ignore'), activities)))
        print(list(filter(lambda x: 'is_default' in x, activities))[0]["name"])
        print(activities)
        print(activities[2])

    def test_Can_Create_Time_Entry(self):
        print("trying to Post an entry")
        result = self.client.post_time_entry(TimeEntry(activity_id=9, issue_id=1, comments="asfads", time_in_minutes="2"))
        assert result
