import unittest
from Client.profile_save import Profile
import os
from Server.player import Player
from os.path import exists


class TestProfileSave(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.profile = Profile(os.path.abspath("Client/Data/test/test_profiles.json"))
        cls.player1 = Player("test", 0, "test", False)
        cls.player2 = Player("test2", 0, "test2", False)

    def setUp(self):
        self.profile.delete_all_profiles()

    def test_all(self):
        if exists(self.profile.path):
            os.remove(self.profile.path)
        data = [self.player1, self.player2]
        self.profile.set_profiles(data)
        self.assertEqual(self.profile.get_profiles(), data)
        self.profile.delete_all_profiles()
        self.assertEqual(self.profile.get_profiles(), [])
