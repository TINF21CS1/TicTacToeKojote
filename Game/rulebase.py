from gamestate import GameState

class RuleBase:
    """
    Represents the rule base for a Tic-Tac-Toe game.

    Args:
        playfield_dimensions (tuple[int, int]): The dimensions of the playfield (default: (3, 3)).

    Attributes:
        playfield_dimensions (tuple[int, int]): The dimensions of the playfield.

    """

    def __init__(self, playfield_dimensions: (int, int) = (3,3)):
        self._playfield_dimensions = playfield_dimensions

    @property
    def playfield_dimensions(self) -> (int, int):
        """
        Get the dimensions of the playfield.

        Returns:
            tuple[int, int]: The dimensions of the playfield.

        """
        return self._playfield_dimensions

    def is_move_valid(self, state: GameState, new_position: (int, int)) -> bool:
        """
        Check if a move is valid.

        Args:
            state (GameState): The current game state.
            new_position (tuple[int, int]): The new position to check.

        Returns:
            bool: True if the move is valid, False otherwise.

        Raises:
            ValueError: If the playfield value is invalid.

        """
        if self.is_game_state_valid(state) == False:
            raise ValueError("Invalid game state")

        if state.playfield_value(new_position) == 0:
            return True
        elif state.playfield_value(new_position) == 1 or state.playfield_value(new_position) == 2:
            return False
        else:
            raise ValueError("Invalid playfield value")

    def check_win(self, state: GameState):
        """
        Check if there is a winner in the current game state.

        Args:
            state (GameState): The current game state.

        Returns:
            None.
            Sets the winner of the game in given state if there is one.
        """
        if self.is_game_state_valid(state) == False:
            raise ValueError("Invalid game state")

        # Check horizontal lines
        for row in state.playfield:
            if len(set(row)) == 1 and row[0] != 0:
                state.set_winner(row[0])
                return

        # Check vertical lines
        for column in state.playfield.T:
            if len(set(column)) == 1 and column[0] != 0:
                state.set_winner(column[0])
                return

        # Check diagonals
        diagonal1 = [state.playfield[i][i] for i in range(min(state.playfield_dimensions))]
        diagonal2 = [state.playfield[i][j] for i, j in zip(range(min(state.playfield_dimensions)), range(max(state.playfield_dimensions)-1, -1, -1))]
        if len(set(diagonal1)) == 1 and diagonal1[0] != 0:
            state.set_winner(diagonal1[0])
            return
        elif len(set(diagonal2)) == 1 and diagonal2[0] != 0:
            state.set_winner(diagonal2[0])
        
        # Check draw
        if 0 not in state.playfield:
            state.set_winner(0)
            return

        return 0

    def is_game_state_valid(self, state: GameState) -> bool:
        """
        Check if the current game state is valid.

        Args:
            state (GameState): The current game state.

        Returns:
            bool: True if the game state is valid, False otherwise.

        """
        count_1 = sum(row.count(1) for row in state.playfield)
        count_2 = sum(row.count(2) for row in state.playfield)
        return abs(count_1 - count_2) <= 1

    def explain(self, state: GameState, prev: (int, int), new: (int, int)) -> str:
        """
        Generate an explanation for a move.

        Args:
            state (GameState): The current game state.
            prev (tuple[int, int]): The previous position.
            new (tuple[int, int]): The new position.

        Returns:
            str: The explanation for the move.

        """
        return ""  # TODO
