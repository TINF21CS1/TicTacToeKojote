from Server.gamestate import GameState
from Server.rulebase import RuleBase
import unittest

class TestRuleBase(unittest.TestCase):
    def setUp(self):
        # Create a GameState object
        self.state = GameState()
        # Create a RuleBase object
        self.rulebase = RuleBase()

    def test_is_move_valid(self):
        # Test case 1: Valid move
        new_position = (0, 0)
        self.assertTrue(self.rulebase.is_move_valid(self.state, new_position))

        # Test case 2: Invalid move (position already occupied)
        self.state.set_player_position(1, new_position)
        self.assertRaises(ValueError, lambda: self.rulebase.is_move_valid(self.state, new_position))

    def test_check_win_1(self):
        # Test case 1: No winner
        self.rulebase.check_win(self.state)
        self.assertEqual(self.state.winner, 0)
        self.assertFalse(self.state.finished)

    def test_check_win_2(self):
        # Test case 2: Horizontal win
        self.state._playfield = [[1, 1, 1], [0, 2, 0], [2, 0, 2]]
        self.rulebase.check_win(self.state)
        self.assertEqual(self.state.winner, 1)
        self.assertTrue(self.state.finished)

    def test_check_win_3(self):
        # Test case 3: Vertical win
        self.state._playfield = [[1, 0, 2], [1, 0, 2], [1, 2, 0]]
        self.rulebase.check_win(self.state)
        self.assertEqual(self.state.winner, 1)
        self.assertTrue(self.state.finished)

    def test_check_win_4(self):
        # Test case 4: Diagonal win
        self.state._playfield = [[1, 0, 2], [2, 1, 0], [2, 0, 1]]
        self.rulebase.check_win(self.state)
        self.assertEqual(self.state.winner, 1)
        self.assertTrue(self.state.finished)

    def test_check_win_5(self):
        # Test case 5: Draw
        self.state._playfield = [[1, 2, 1], [1, 2, 2], [2, 1, 1]]
        self.rulebase.check_win(self.state)
        self.assertEqual(self.state.winner, 0)
        self.assertTrue(self.state.finished)

    def test_check_win_6(self):
        # Test case 6: Player 2 win
        self.state._playfield = [[1, 1, 2], [2, 2, 1], [2, 1, 0]]
        self.rulebase.check_win(self.state)
        self.assertEqual(self.state.winner, 2)
        self.assertTrue(self.state.finished)

    def test_is_game_state_valid(self):
        # Test case 1: Valid game state
        self.assertTrue(self.rulebase.is_game_state_valid(self.state))

        # Test case 2: Invalid game state (difference in player counts > 1)
        self.state.set_player_position(1, (0, 0))
        self.state.set_player_position(1, (0, 1))
        self.assertFalse(self.rulebase.is_game_state_valid(self.state))

# Run the test cases
if __name__ == '__main__':
    unittest.main()
