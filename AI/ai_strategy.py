from abc import ABC, abstractmethod
from Client.client import GameClient
from Server.player import Player
from Server.rulebase import RuleBase
from Server.gamestate import GameState
import asyncio
import random

class AIStrategy(ABC, GameClient):

    def __init__(self):
        _strength = "Placeholder"
        _good_luck_message = "Good luck!"
        _good_game_message_lost = "Good game! You played well."
        _good_game_message_won = "Good game! I'll have better luck next time."
        _good_game_message_draw = "Good game! We are evenly matched."
        _ai_uuid = "108eaa05-2b0e-4e00-a190-8856edcd56a5"
        _rulebase = RuleBase()

    def thread_entry(self):
        asyncio.run(self.run())

    async def run(self):

        # The AI-UUID is hardcoded so that it can be excluded from statistics
        await self.join_game(Player(f"{self._strength} AI", random.randint(0, 0xFFFFFF)), "localhost", uuid=self._ai_uuid)
        await self.lobby_ready()


    async def _message_handler(self, message_type: str):
        
        match message_type:
            case "lobby/status":
                # AI does not need this
                pass
            case "game/start":
                self.wish_good_luck()
            
            case "game/end":
                self.say_good_game()

            case "game/turn":
                if self._current_player.uuid == self._ai_uuid:
                    self.update_gamestate()
                    self.do_turn()
                
            case "statistics/statistics":
                # AI does not need this
                pass
            case "game/error":
                # AI does not need this
                pass
            case "chat/receive":
                # AI does not need this
                pass
        
        return

    def wish_good_luck(self):
        self.chat_message(self._good_luck_message)

    def say_good_game(self):
        if self._winner.uuid == self._ai_uuid:
            self.chat_message(self._good_game_message_won)
        elif self._winner.uuid == None:
            self.chat_message(self._good_game_message_draw)
        else:
            self.chat_message(self._good_game_message_lost)

    def get_empty_cells(self, game_status: list):
        """
        Get a list of all empty cells in the current game state.
        """
        empty_cells = []
        for i, row in enumerate(game_status):
            for j, cell in enumerate(row):
                if cell == 0:
                    empty_cells.append((i, j))
        return empty_cells

    @abstractmethod
    async def do_turn(self):
        pass

        

class WeakAIStrategy(AIStrategy):
    
    def __init__(self):
        _strength = "Weak"
        _good_luck_message = "Good luck! I'm still learning so please have mercy on me."
        _good_game_message_lost = "Good game! I will try to do better next time."
        _good_game_message_won = "Good game! I can't believe I won!"
        _good_game_message_draw = "Good game! I' happy I didn't lose."
    
    async def do_turn(self):

        empty_cells = self.get_empty_cells(self._game_status)
        move = random.randint(0, len(empty_cells) - 1)
        await self.game_make_move(empty_cells[move][0], empty_cells[move][1])

class AdvancedAIStrategy(AIStrategy):

    def __init__(self):
        _strength = "Advanced"
        _good_luck_message = "Good luck! I hope you are ready for a challenge."
        _good_game_message_lost = "Good game! I admire your skills."
        _good_game_message_won = "Good game! I hope you learned something from me."
        _good_game_message_draw = "Good game! I hope you are ready for a rematch."

    async def do_turn(self):
        """
        Advanced AI Logic:
        1. Make a move if there is a winning move
        2. Block the opponent if there is a winning move
        3. Make a random move(or maybe more complex logic)
        """

        empty_cells = self.get_empty_cells(self._game_status)

        # Check for own winning move
        for possible_move in empty_cells:
            temp_gamestate = GameState()

            # Make deep copy of the game state
            temp_gamestate._playfield = [self._game_status[row].copy() for row in self._game_status]

            temp_gamestate.set_player_position(self._player_number, possible_move)
            RuleBase.check_win(temp_gamestate)
            if temp_gamestate.winner == self._player_number:
                await self.game_make_move(possible_move[0], possible_move[1])
                return
            
        # Check for opponent winning move
        for possible_move in empty_cells:
            temp_gamestate = GameState()

            # Make deep copy of the game state
            temp_gamestate._playfield = [self._game_status[row].copy() for row in self._game_status]

            temp_gamestate.set_player_position(self._opponent_number, possible_move)
            RuleBase.check_win(temp_gamestate)
            if temp_gamestate.winner == self._opponent_number:
                await self.game_make_move(possible_move[0], possible_move[1])
                return
            
        # Make a random move
        move = random.randint(0, len(empty_cells) - 1)
        await self.game_make_move(empty_cells[move][0], empty_cells[move][1])
