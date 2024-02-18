from player import Player
from gamestate import GameState
from rulebase import RuleBase

class Game:
    def __init__(self, player1: Player, player2: Player, rule_base: RuleBase = RuleBase()):
        """
        Initializes a new instance of the Game class.

        Args:
            player1 (Player): The first player.
            player2 (Player): The second player.
            rule_base (RuleBase, optional): The rule base for the game. Defaults to RuleBase().
        """
        self._id: int = 1 #TODO count up
        self.state = GameState()
        self.players: list = [None, player1, player2]
        self.rule_base = rule_base

    def move(self, player: int, new_position: (int, int)) -> Player | None:
        """
        Makes a move in the game.

        Args:
            player (int): The player making the move.
            new_position ((int, int)): The new position to place the player's move.

        Returns:
            Player | None: The winning player if a move made them win, otherwise None.
        
        Raises:
            ValueError: If the move is illegal.
        """
        if not self.rule_base.is_move_valid(self.state, new_position):
            raise ValueError("Illegal move")
        
        self.state.set_player_position(player, new_position)

        if winner := (self.rule_base.check_win(self.state) != 0):
            return self.players[winner]
        else:
            return None
