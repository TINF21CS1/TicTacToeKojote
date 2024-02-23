from player import Player
from gamestate import GameState
from rulebase import RuleBase
import uuid

class Game:
    def __init__(self, player1: Player, player2: Player, rule_base: RuleBase = RuleBase()):
        """
        Initializes a new instance of the Game class.

        Args:
            player1 (Player): The first player.
            player2 (Player): The second player.
            rule_base (RuleBase, optional): The rule base for the game. Defaults to RuleBase().
        """
        self._uuid: uuid.UUID = uuid.uuid4()
        self._id: int =  self._uuid.int
        self.state = GameState()
        self.players: list = [None, player1, player2]
        self.rule_base = rule_base

    def move(self, player: int, new_position: tuple[int, int]):
        """
        Makes a move in the game.

        Args:
            player (int): The player making the move.
            new_position (tuple[int, int]): The new position to place the player's move.
        
        Raises:
            ValueError: If the move is illegal.
        """
        try:
            self.rule_base.is_move_valid(self.state, new_position)
            self.state.set_player_position(player, new_position)
        except ValueError as e:
            # TODO: Call a function in networking to display the error
            print(e)
        
    @property
    def current_player_uuid(self) -> str:
        """
        Returns the UUID string of the current player.

        Returns:
            str: The UUID string of the current player.
        """
        return str(self.players[self.state.current_player].uuid)