from gamestate import GameState
from rulebase import RuleBase

def test_is_move_valid():
    # Create a GameState object
    state = GameState()

    # Create a RuleBase object
    rulebase = RuleBase()

    # Test case 1: Valid move
    new_position = (0, 0)
    assert rulebase.is_move_valid(state, new_position) == True

    # Test case 2: Invalid move (position already occupied)
    state.set_player_position(1, new_position)
    assert rulebase.is_move_valid(state, new_position) == False

def test_check_win():

    # Test case 1: No winner
    state = GameState()
    rulebase = RuleBase()
    rulebase.check_win(state)
    assert state.winner == 0 & state.finished == False

    # Test case 2: Horizontal win
    state = GameState()
    rulebase = RuleBase()
    state._playfield = [[1, 1, 1], [0, 2, 0], [2, 0, 2]]
    rulebase.check_win(state)
    assert state.winner == 1 & state.finished == True

    # Test case 3: Vertical win
    state = GameState()
    rulebase = RuleBase()
    state._playfield = [[1, 0, 2], [1, 0, 2], [1, 2, 0]]
    rulebase.check_win(state)
    assert state.winner == 1 & state.finished == True

    # Test case 4: Diagonal win
    state = GameState()
    rulebase = RuleBase()
    state._playfield = [[1, 0, 2], [2, 1, 0], [2, 0, 1]]
    rulebase.check_win(state)
    assert state.winner == 1 & state.finished == True

    # Test case 5: Draw
    state = GameState()
    rulebase = RuleBase()
    state._playfield = [[1, 2, 1], [1, 2, 2], [2, 1, 1]]
    rulebase.check_win(state)
    assert state.winner == 0 and state.finished == True

def test_is_game_state_valid():
    # Create a GameState object
    state = GameState()

    # Create a RuleBase object
    rulebase = RuleBase()

    # Test case 1: Valid game state
    assert rulebase.is_game_state_valid(state) == True

    # Test case 2: Invalid game state (difference in player counts > 1)
    state.set_player_position(1, (0, 0))
    state.set_player_position(1, (0, 1))
    assert rulebase.is_game_state_valid(state) == False

# Run the test cases
test_is_move_valid()
test_check_win()
test_is_game_state_valid()
