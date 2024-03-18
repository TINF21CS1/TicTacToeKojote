import unittest
from Client.profile_save import Profile
from Server.player import Player
from uuid import uuid4

class TestProfileSave(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("test", 0, uuid4(), False)
        self.player2 = Player("test2", 0, uuid4(), False)
        Profile.delete_all_profiles()

    def test_all(self):
        data = ([self.player1, self.player2], 0)
        Profile.set_profiles(data[0], data[1])
        self.assertEqual(Profile.get_profiles(), data)
        Profile.delete_all_profiles()
        self.assertEqual(Profile.get_profiles(), ([], 0))
