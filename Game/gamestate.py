class GameState:
    _playfiled: [int][int]
    _current_player: int
    _finished: bool
    _winner: int

    def __init__(self, starting_player: int, playfiled_dimensions: (int, int) = (3,3)):
        self._playfiled = [[0 for _ in range(playfiled_dimensions[0])] for _ in range(playfiled_dimensions[1])]
        self._current_player = starting_player
        self._finished = False
        self._winner = 0
    
    def set_player_position(player: int, new_position: (int, int)):
        pass #TODO

    def set_winnter(winner: int):
        self._finished = True
        self._winner = winner
    
    @property
    def winner() -> int:
        return self._winner
    
    @property
    def finished() -> bool:
        return self._finished
    
    @property
    def current_player() -> int:
        return self._current_player

    @property
    def playfield(self) -> [int][int]:
        return self._playfiled
