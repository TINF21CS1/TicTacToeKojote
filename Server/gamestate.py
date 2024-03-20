import random

class GameState:
    """
    Represents the state of a Tic-Tac-Toe game.

    Parameters:
        playfield_dimensions (tuple[int, int]): The dimensions of the playfield (default: (3, 3)).

    Properties:
        winner (int): The index of the winning player.
        finished (bool): True if the game has finished, False otherwise.
        playfield (list[list[int]]): The playfield of the game.
        current_player (int): The index of the current player.
        playfield_dimensions (tuple[int, int]): The dimensions of the playfield.

    Methods:
        set_player_position(self, player: int, new_position: (int, int)): Sets the position of a player on the playfield.
        set_winner(self, winner: int): Sets the winner of the game.
        playfield_value(self, position: (int, int)): Returns the value at the specified position on the playfield.
    """

    _playfield: list[list[int]]
    _finished: bool
    _winner: int = None
    _current_player: int = None

    def __init__(self, playfield_dimensions: tuple[int, int] = (3,3)):
        """
        Initializes a new instance of the GameState class.

        Args:
            playfield_dimensions (tuple[int, int], optional): The dimensions of the playfield. Defaults to (3, 3).
        """
        self._playfield = [[0 for _ in range(playfield_dimensions[0])] for _ in range(playfield_dimensions[1])]
        self._finished = False
        self._winner = 0
        self._current_player = 1
    
    def set_player_position(self, player: int, new_position: tuple[int, int]):
        """
        Sets the position of a player on the playfield.

        Args:
            player (int): The number of the player.
            new_position (tuple[int, int]): The new position set by the player on the playfield.
        """
        self._playfield[new_position[0]][new_position[1]] = player
        self._current_player = 1 if player == 2 else 2

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

    @property
    def playfield_dimensions(self) -> tuple[int, int]:
        """
        Returns the size of the playfield.

        Returns:
            tuple[int, int]: The size of the playfield.
        """
        return (len(self._playfield), len(self._playfield[0]))
    
    @property
    def current_player(self) -> int:
        """
        Returns the id of the current player.

        Returns:
            int: The id of the current player.
        """
        return self._current_player
