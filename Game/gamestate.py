class GameState:
    """
    Represents the state of a Tic-Tac-Toe game.

    Attributes:
        _playfield (list[list[int]]): The playfield of the game, represented as a 2D list.
        _finished (bool): Indicates whether the game has finished.
        _winner (int): The number of the winning player, if any.

    Methods:
        __init__(self, starting_player: int, playfiled_dimensions: (int, int) = (3,3)): Initializes a new instance of the GameState class.
        set_player_position(self, player: int, new_position: (int, int)): Sets the position of a player on the playfield.
        set_winner(self, winner: int): Sets the winner of the game.
        winner(self) -> int: Returns the number of the winning player.
        finished(self) -> bool: Returns True if the game has finished, False otherwise.
        playfield(self) -> list[list[int]]: Returns the playfield of the game.
        playfield_value(self, position: (int, int)) -> int: Returns the value at the specified position on the playfield.
    """

    _playfield: list[list[int]]
    _finished: bool
    _winner: int

    def __init__(self, playfiled_dimensions: tuple[int, int] = (3,3)):
        """
        Initializes a new instance of the GameState class.

        Args:
            playfiled_dimensions (tuple[int, int], optional): The dimensions of the playfield. Defaults to (3, 3).
        """
        self._playfield = [[0 for _ in range(playfiled_dimensions[0])] for _ in range(playfiled_dimensions[1])]
        self._finished = False
        self._winner = 0
    
    def set_player_position(self, player: int, new_position: tuple[int, int]):
        """
        Sets the position of a player on the playfield.

        Args:
            player (int): The number of the player.
            new_position (tuple[int, int]): The new position set by the player on the playfield.
        """
        self._playfield[new_position[0]][new_position[1]] = player

    def set_winner(self, winner: int):
        """
        Sets the winner of the game.

        Args:
            winner (int): The id of the winning player. 0 if draw.
        """
        self._finished = True
        self._winner = winner
    
    @property
    def winner(self) -> int:
        """
        Returns the id of the winning player.

        Returns:
            int: The id of the winning player.
        """
        return self._winner
    
    @property
    def finished(self) -> bool:
        """
        Returns True if the game has finished, False otherwise.

        Returns:
            bool: True if the game has finished, False otherwise.
        """
        return self._finished
    
    @property
    def playfield(self) -> list[list[int]]:
        """
        Returns the playfield of the game.

        Returns:
            list[list[int]]: The playfield of the game.
        """
        return self._playfield

    def playfield_value(self, position: tuple[int, int]) -> int:
        """
        Returns the value at the specified position on the playfield.

        Args:
            position (tuple[int, int]): The position on the playfield.

        Returns:
            int: The value at the specified position on the playfield.
        """
        return self._playfield[position[0]][position[1]]
