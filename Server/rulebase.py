from Server.gamestate import GameState

class RuleBase:
    """
    Represents the rule base for a Tic-Tac-Toe game.

    Parameters:
        playfield_dimensions (tuple[int, int]): The dimensions of the playfield (default: (3, 3)).

    Attributes:
        playfield_dimensions (tuple[int, int]): The dimensions of the playfield.

    Functions:
        is_move_valid(state: GameState, new_position: tuple[int, int]) -> bool: Check if a move is valid.
        check_win(state: GameState) -> None: Check if there is a winner in the current game state.
        is_game_state_valid(state: GameState) -> bool: Check if the current game state is valid.
    """

    def __init__(self, playfield_dimensions: tuple[int, int] = (3,3)):
        self._playfield_dimensions = playfield_dimensions

    @property
    def playfield_dimensions(self) -> tuple[int, int]:
        """
        Get the dimensions of the playfield.

        Returns:
            tuple[int, int]: The dimensions of the playfield.

        """
        return self._playfield_dimensions

    def is_move_valid(self, state: GameState, new_position: tuple[int, int]) -> bool:
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
            raise ValueError("Invalid game state. This should not happen and should be investigated.")

        if state.playfield_value(new_position) == 0:
            return True
        elif state.playfield_value(new_position) == 1 or state.playfield_value(new_position) == 2:
            raise ValueError(f"The space ({new_position[0]}, {new_position[1]}) is already taken. Pick a free space!")
        else:
            raise ValueError("Invalid playfield value. This should not happen and should be investigated.")

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
        for column in transpose(state.playfield):
            if len(set(column)) == 1 and column[0] != 0:
                state.set_winner(column[0])
                return

        # Check diagonals
        if state.playfield_dimensions[0] != state.playfield_dimensions[1]:
            # playfield is not square and thus has no diagonal winning condition
            return

        diagonal1 = [state.playfield[i][i] for i in range(state.playfield_dimensions[0])]
        diagonal2 = [state.playfield[i][j] for i,j in zip(range(state.playfield_dimensions[0]), range(state.playfield_dimensions[0]-1, -1, -1))]
        if len(set(diagonal1)) == 1 and diagonal1[0] != 0:
            state.set_winner(diagonal1[0])
            return
        elif len(set(diagonal2)) == 1 and diagonal2[0] != 0:
            state.set_winner(diagonal2[0])
            return
        
        # Check draw
        if 0 not in [item for row in state.playfield for item in row]:
            state.set_winner(0)
            return

        return

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

def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """
    Transpose a matrix.

    Args:
        matrix (list[list[int]]): The matrix to transpose.

    Returns:
        list[list[int]]: The transposed matrix.

    """
    return [list(row) for row in zip(*matrix)]
