import unittest
from Client.profile_save import Profile
import os
from Server.player import Player


class TestProfileSave(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.profile = Profile(os.path.abspath("Client/Data/test/test_profiles.json"))
        cls.player1 = Player("test", 0, "test", False)
        cls.player2 = Player("test2", 0, "test2", False)

    def setUp(self):
        self.profile.delete_all_profiles()

    def test_get_profile_by_name(self):
        self.profile.add_new_profile(self.player1)
        self.assertEqual(self.profile.get_profile_by_name(self.player1),
                         self.player1)
        self.profile.delete_all_profiles()
        self.assertEqual(self.profile.get_profiles(), [])

    def test_get_profile_by_uuid(self):
        self.profile.add_new_profile(self.player1)
        self.assertEqual(self.profile.get_profile(self.player1),
                         self.player1)
        self.profile.delete_all_profiles()
        self.assertEqual(self.profile.get_profiles(), [])
    def test_add_new_profile(self):
        self.profile.add_new_profile(self.player1)
        self.assertEqual(self.profile.get_profile(self.player1),
                         self.player1)
        self.profile.delete_all_profiles()
        self.assertEqual(self.profile.get_profiles(), [])

    def test_delete_profile(self):
        self.profile.add_new_profile(self.player1)
        self.profile.add_new_profile(self.player2)
        self.profile.delete_profile(self.player1)
        self.assertEqual(self.profile.get_profiles(), [self.player2])
        self.profile.delete_all_profiles()

    def test_delete_profile_by_name(self):
        self.profile.add_new_profile(self.player1)
        self.profile.add_new_profile(self.player2)
        self.profile.delete_profile_by_name(self.player1)
        self.assertEqual(self.profile.get_profiles(), [self.player2])
        self.profile.delete_all_profiles()

    def test_set_profiles(self):
        data = [self.player1, self.player2]
        self.profile.set_profiles(data)
        self.assertEqual(self.profile.get_profiles(), data)
        self.profile.delete_all_profiles()