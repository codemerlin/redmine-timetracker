import unittest
from RedMineClient import RedMineClient


class RedMineClientTests(unittest.TestCase):
    def setUp(self):
        self.client = RedMineClient("https://support.targetintegration.com", "c3a7f2f4562ed90ff5bc9b6d9e0574f4d434d54e")
        pass

    def test_getIssue(self):
        issue = self.client.get_issue(1)
        self.assertIsNotNone(issue)
        print(issue)
