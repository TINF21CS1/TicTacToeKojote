from Server.rulebase import RuleBase, transpose
from Server.gamestate import GameState

class AIRulebase(RuleBase):
    # overwrite the check_win method without checking if the playfield
    # is valid because the AI wants to check whether the next move of the opponent will lead to a win
    def check_win(self, state: GameState):

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
        diagonal2 = [state.playfield[i][j] for i in range(state.playfield_dimensions[0]) for j in range(state.playfield_dimensions[0], -1)]
        if len(set(diagonal1)) == 1 and diagonal1[0] != 0:
            state.set_winner(diagonal1[0])
            return
        elif len(set(diagonal2)) == 1 and diagonal2[0] != 0:
            state.set_winner(diagonal2[0])
        
        # Check draw
        if 0 not in [item for row in state.playfield for item in row]:
            state.set_winner(0)
            return

        return

