from typing import Any
from gamestate import GameState

class RuleBase:
    def __init__(self, playfield_dimensions: (int, int) = (3,3)):
        self._playfiled_dimensions = playfield_dimensions

    @property
    def playfield_dimensions(self) -> (int, int):
        return self._playfiled_dimensions

    def is_move_valid(self, state: GameState, new_position: (int, int)) -> bool:
        if state.playfield_value(new_position) == 0:
            return True
        elif state.playfield_value(new_position) == 1 or state.playfield_value(new_position) == 2:
            return False
        else:
            raise ValueError("Invalid playfield value")
    
    # returns the winning player id
    def check_win(self, state: GameState) -> int:
        return self._check_win_horizontal(state) or self._check_win_vertical(state) or self._check_win_diagonal(state)
    
    def _check_win_horizontal(self, state: GameState) -> int:
        for row in state.playfield:
            if row[0] == row[1] == row[2] and row[0] != 0:
                return row[0]
        return 0
    
    def _check_win_vertical(self, state: GameState) -> int:
        for i in range(3):
            if state.playfield[0][i] == state.playfield[1][i] == state.playfield[2][i] and state.playfield[0][i] != 0:
                return state.playfield[0][i]
        return 0
    
    def _check_win_diagonal(self, state: GameState) -> int:
        if state.playfield[0][0] == state.playfield[1][1] == state.playfield[2][2] and state.playfield[0][0] != 0:
            return state.playfield[0][0]
        elif state.playfield[0][2] == state.playfield[1][1] == state.playfield[2][0] and state.playfield[0][2] != 0:
            return state.playfield[0][0]
        return 0        
    
    def is_game_state_valid(self, state: GameState) -> bool:
        return True #TODO
    
    def explain(self, state: GameState, prev: (int, int), new: (int, int)) -> str:
        return "" #TODO
