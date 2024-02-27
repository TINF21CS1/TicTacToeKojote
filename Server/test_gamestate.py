from Server.gamestate import GameState
import unittest

class TestGameState(unittest.TestCase):
    def setUp(self):
        # Create a GameState object
        self.state = GameState()

    def test_set_player_position(self):
        # Test case 1: Set player position
        new_position = (0, 0)
        self.state.set_player_position(1, new_position)
        self.assertEqual(self.state.playfield_value(new_position), 1)

    def test_set_winner(self):
        # Test case 1: Set winner
        self.state.set_winner(1)
        self.assertEqual(self.state.winner, 1)
        self.assertTrue(self.state.finished)

    def test_playfield(self):
        # Test case 1: Check playfield
        self.assertEqual(self.state.playfield, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def test_playfield_value(self):
        # Test case 1: Check playfield value
        position = (0, 0)
        self.assertEqual(self.state.playfield_value(position), 0)

# Run the test cases
if __name__ == '__main__':
    unittest.main()