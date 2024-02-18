from gamestate import GameState

def test_set_player_position():
    # Create a GameState object
    state = GameState()

    # Test case 1: Set player position
    new_position = (0, 0)
    state.set_player_position(1, new_position)
    assert state.playfield_value(new_position) == 1

def test_set_winner():
    # Create a GameState object
    state = GameState()

    # Test case 1: Set winner
    state.set_winner(1)
    assert state.winner == 1
    assert state.finished == True

def test_playfield():
    # Create a GameState object
    state = GameState()

    # Test case 1: Check playfield
    assert state.playfield == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

def test_playfield_value():
    # Create a GameState object
    state = GameState()

    # Test case 1: Check playfield value
    position = (0, 0)
    assert state.playfield_value(position) == 0

# Run the test cases
test_set_player_position()
test_set_winner()
test_playfield()
test_playfield_value()