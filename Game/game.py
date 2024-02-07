class Game:
    def __init__(self, player1: Player, player2: Player, rule_base: RuleBase = RuleBase()):
        self._id: int = 1 #TODO count up
        self.state = GameState()
        self.players: dict = (
            player1: 1,
            player2: 1
        )
        self.rule_base = rule_base

    # returns player if move made win.
    # throws illegal move error on illegal move
    def move(player: Player, new_position: (int, int)) -> Player:
        pass
