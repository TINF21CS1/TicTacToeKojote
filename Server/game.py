from Server.player import Player
from Server.gamestate import GameState
from Server.rulebase import RuleBase
import uuid
from random import shuffle

class Game:
    """
    Initializes a new instance of the Game class.

    Parameters:
        player1 (Player): The first player.
        player2 (Player): The second player.
        rule_base (RuleBase, optional): The rule base for the game. Defaults to RuleBase().

    Properties:
        current_player_uuid (str): The UUID string of the current player.
        winner (Player): The winner of the game.
    
    Methods:
        move(self, player: int, new_position: tuple[int, int]): Makes a move in the game.
    """

    def __init__(self, player1: Player, player2: Player, rule_base: RuleBase = RuleBase()):
        self._uuid: uuid.UUID = uuid.uuid4()
        self._id: int =  self._uuid.int
        self.state = GameState()
        players = [player1, player2]
        shuffle(players)
        self.players: list = [None] +  players
        self.rule_base = rule_base

    def move(self, player: int, new_position: tuple[int, int]):
        """
        Makes a move in the game.

        Parameters::
            player (int): The player making the move.
            new_position (tuple[int, int]): The new position to place the player's move.
        
        Raises:
            ValueError: If the move is illegal.
        """
        try:
            self.rule_base.is_move_valid(self.state, new_position)
            self.state.set_player_position(player, new_position)
            self.rule_base.check_win(self.state)
        except ValueError as e:
            raise ValueError(e)

    @property
    def current_player_uuid(self) -> str:
        """
        Returns the UUID string of the current player.

        Returns:
            str: The UUID string of the current player.
        """
        return str(self.players[self.state.current_player].uuid)
    
    @property
    def winner(self) -> Player:
        """
        Returns the winner of the game.

        Returns:
            Player: The winner of the game.
        """
        return self.players[self.state.winner]