import unittest
from uuid import UUID
import os

from Server.statistics import Statistics
from Server.player import Player

class TestStatistics(unittest.TestCase):
    def setUp(self):
        # Create a Statistics object
        self.stats = Statistics()
    
    def tearDown(self):
        # Clean up the database after each test
        self.stats.conn.close()
        os.remove(self.stats.path)

    def test_get_statistics(self):
        # Test case 1: Empty statistics
        self.assertEqual(self.stats.get_statistics(), [])

        # Test case 2: Non-empty statistics
        # Add some profiles to the database
        self.stats._add_profile(Player("TestplayerOne", 3319955, UUID('1f73adf1-4568-4d79-8be9-b76137c92d73')))
        self.stats._add_profile(Player("TestplayerTwo", 3319955, UUID('ff3c5d77-447c-449b-a58f-924756e4720a')))
        self.stats._add_profile(Player("TestplayerThree", 3319955, UUID('278cb502-00c0-45e4-8a7f-d9c8e85ae70a')))
        self.assertEqual(len(self.stats.get_statistics()), 3)

    def test_increment_emojis(self):
        # Test case 1: Increment emojis for existing profile
        player = Player("TestplayerOne", 3319955, UUID('1f73adf1-4568-4d79-8be9-b76137c92d73'))
        self.stats._add_profile(player)
        self.stats.increment_emojis(player, "Hello 😀👍")
        self.assertEqual(self.stats.get_statistics()[0][7], 2)

        # Test case 2: Increment emojis for non-existing profile
        player = Player("TestplayerTwo", 3319955, UUID('ff3c5d77-447c-449b-a58f-924756e4720a'))
        self.stats.increment_emojis(player, "Hello 😀👍")
        self.assertEqual(self.stats.get_statistics()[1][7], 2)

    def test_increment_moves(self):
        # Test case 1: Increment moves for existing profile
        player = Player("TestplayerOne", 3319955, UUID('1f73adf1-4568-4d79-8be9-b76137c92d73'))
        self.stats._add_profile(player)
        self.stats.increment_moves(player)
        self.assertEqual(self.stats.get_statistics()[0][6], 1)

        # Test case 2: Increment moves for non-existing profile
        player = Player("TestplayerTwo", 3319955, UUID('ff3c5d77-447c-449b-a58f-924756e4720a'))
        self.stats.increment_moves(player)
        self.assertEqual(self.stats.get_statistics()[1][6], 1)

    def test_increment_games(self):
        # Test case 1: Draw game
        player1 = Player("TestplayerOne", 3319955, UUID('1f73adf1-4568-4d79-8be9-b76137c92d73'))
        player2 = Player("TestplayerTwo", 3319955, UUID('ff3c5d77-447c-449b-a58f-924756e4720a'))
        self.stats._add_profile(player1)
        self.stats._add_profile(player2)
        self.stats.increment_games([None, player1, player2], 0)
        self.assertEqual(self.stats.get_statistics()[0][5], 1)
        self.assertEqual(self.stats.get_statistics()[1][5], 1)

        # Test case 2: Player 1 wins
        self.stats.increment_games([None, player1, player2], 1)
        self.assertEqual(self.stats.get_statistics()[0][3], 1)
        self.assertEqual(self.stats.get_statistics()[1][4], 1)

        # Test case 3: Player 2 wins
        self.stats.increment_games([None, player1, player2], 2)
        self.assertEqual(self.stats.get_statistics()[0][4], 1)
        self.assertEqual(self.stats.get_statistics()[1][3], 1)

    def test_check_profile(self):
        # Test case 1: Check if profile exists (existing profile)
        player = Player("TestplayerOne", 3319955, UUID('1f73adf1-4568-4d79-8be9-b76137c92d73'))
        self.stats._add_profile(player)
        self.assertTrue(self.stats._check_profile('1f73adf1-4568-4d79-8be9-b76137c92d73'))

        # Test case 2: Check if profile exists (non-existing profile)
        self.assertFalse(self.stats._check_profile('ff3c5d77-447c-449b-a58f-924756e4720a'))

# Run the test cases
if __name__ == '__main__':
    unittest.main()