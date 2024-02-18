from gamestate import GameState

class RuleBase:
    def __init__(self, playfield_dimensions: (int, int) = (3,3)):
        self._playfield_dimensions = playfield_dimensions

    @property
    def playfield_dimensions(self) -> (int, int):
        return self._playfield_dimensions

    def is_move_valid(self, state: GameState, new_position: (int, int)) -> bool:
        if state.playfield_value(new_position) == 0:
            return True
        elif state.playfield_value(new_position) == 1 or state.playfield_value(new_position) == 2:
            return False
        else:
            raise ValueError("Invalid playfield value")
    
    # returns the winning player id
    def check_win(self, state: GameState) -> int:
        # Check horizontal lines
        for row in state.playfield:
            if len(set(row)) == 1 and row[0] != 0:
                return row[0]

        # Check vertical lines
        for column in state.playfield.T:
            if len(set(column)) == 1 and column[0] != 0:
                return column[0]

        # Check diagonals
        diagonal1 = [state.playfield[i][i] for i in range(min(state.playfield_dimensions))]
        diagonal2 = [state.playfield[i][j] for i, j in zip(range(min(state.playfield_dimensions)), range(max(state.playfield_dimensions)-1, -1, -1))]
        if len(set(diagonal1)) == 1 and diagonal1[0] != 0:
            return diagonal1[0]
        elif len(set(diagonal2)) == 1 and diagonal2[0] != 0:
            return diagonal2[0]

        return 0

    def is_game_state_valid(self, state: GameState) -> bool:
        return True #TODO
    
    def explain(self, state: GameState, prev: (int, int), new: (int, int)) -> str:
        return "" #TODO
