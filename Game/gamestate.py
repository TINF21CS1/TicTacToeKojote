class GameState:
    _playfield: [int][int]
    _current_player: int
    _finished: bool
    _winner: int

    def __init__(self, starting_player: int, playfiled_dimensions: (int, int) = (3,3)):
        self._playfield = [[0 for _ in range(playfiled_dimensions[0])] for _ in range(playfiled_dimensions[1])]
        self._current_player = starting_player
        self._finished = False
        self._winner = 0
    
    def set_player_position(self, player: int, new_position: (int, int)):
        self._playfield[new_position[0]][new_position[1]] = player

    def set_winner(self, winner: int):
        self._finished = True
        self._winner = winner
    
    @property
    def winner(self) -> int:
        return self._winner
    
    @property
    def finished(self) -> bool:
        return self._finished
    
    @property
    def current_player(self) -> int:
        return self._current_player

    @property
    def playfield(self) -> [int][int]:
        return self._playfield

    # returns 0 if empty, 1 if player 1, 2 if player 2
    @property
    def playfield_value(self, position: (int, int)) -> int:
        return self._playfield[position[0]][position[1]]
