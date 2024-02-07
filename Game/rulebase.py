class RuleBase:
    def __init__(self, playfield_dimensions: (int, int) = (3,3)):
        self._playfiled_dimensions = playfield_dimensions

    @property
    def playfield_dimensions(self) -> (int, int):
        return self._playfiled_dimensions

    def is_move_valid(self, state: GameState, prev: (int, int), new: (int, int)) -> bool:
        return True #TODO
    
    def is_game_state_valid(self, state: GameState) -> bool:
        return True #TODO
    
    def explain(self, state: GameState, prev: (int, int), new: (int, int)) -> str:
        return "" #TODO
