import unittest
from profile_save import Profile


class TestProfileSave(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.profile = Profile("../json_schema/test/test_profiles.json")

    def setUp(self):
        self.profile.delete_all_profiles()

    def test_get_profile_by_name(self):
        self.profile.add_new_profile("test", "test", "test")
        self.assertEqual(self.profile.get_profile_by_name("test"),
                         {"profile_name": "test", "profile_uuid": "test", "profile_color": "test"})
        self.profile.delete_all_profiles()

    def test_get_profile_by_uuid(self):
        self.profile.add_new_profile("test", "test", "test")
        self.assertEqual(self.profile.get_profile("test"),
                         {"profile_name": "test", "profile_uuid": "test", "profile_color": "test"})
        self.profile.delete_all_profiles()