import unittest
from Client.profile_save import Profile
import os

#todo kda durch 0 teilen fixen

class TestProfileSave(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.profile = Profile(os.path.abspath("json_schema/test/test_profiles.json"))

    def setUp(self):
        self.profile.delete_all_profiles()

    def test_get_profile_by_name(self):
        self.profile.add_new_profile("test", "test", "test")
        self.assertEqual(self.profile.get_profile_by_name("test"),
                         {"profile_name": "test", "profile_uuid": "test", "profile_color": "test"})
        self.profile.delete_all_profiles()
        self.assertEqual(self.profile.get_profiles(), [])

    def test_get_profile_by_uuid(self):
        self.profile.add_new_profile("test", "test", "test")
        self.assertEqual(self.profile.get_profile("test"),
                         {"profile_name": "test", "profile_uuid": "test", "profile_color": "test"})
        self.profile.delete_all_profiles()
        self.assertEqual(self.profile.get_profiles(), [])
    def test_add_new_profile(self):
        self.profile.add_new_profile("test", "test", "test")
        self.assertEqual(self.profile.get_profile("test"),
                         {"profile_name": "test", "profile_uuid": "test", "profile_color": "test"})
        self.profile.delete_all_profiles()
        self.assertEqual(self.profile.get_profiles(), [])

    def test_delete_profile(self):
        self.profile.add_new_profile("test", "test", "test")
        self.profile.add_new_profile("test2", "test", "test")
        self.profile.delete_profile("test")
        self.assertEqual(self.profile.get_profiles(), [{"profile_name": "test2", "profile_uuid": "test", "profile_color": "test"}])
        self.profile.delete_all_profiles()

    def test_delete_profile_by_name(self):
        self.profile.add_new_profile("test", "test", "test")
        self.profile.add_new_profile("test2", "test", "test")
        self.profile.delete_profile_by_name("test")
        self.assertEqual(self.profile.get_profiles(), [{"profile_name": "test2", "profile_uuid": "test", "profile_color": "test"}])
        self.profile.delete_all_profiles()
