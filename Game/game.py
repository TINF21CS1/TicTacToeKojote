from player import Player
from gamestate import GameState
from rulebase import RuleBase

class Game:
    def __init__(self, player1: Player, player2: Player, rule_base: RuleBase = RuleBase()):
        self._id: int = 1 #TODO count up
        self.state = GameState()
        self.players: dict = [player1, player2]
        self.rule_base = rule_base

    # returns player if move made win.
    # throws illegal move error on illegal move
    def move(self, player: int, new_position: (int, int)) -> Player:
        if not self.rule_base.is_move_valid(self.state, new_position):
            raise ValueError("Illegal move")
        
        self.state.set_player_position(player, new_position)

        if winner := (self.rule_base.check_win(self.state) != 0):
            self.state.set_winner(winner)
            return self.players[winner]
        else:
            return None
