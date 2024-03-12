from abc import ABC, abstractmethod
from Client.client import GameClient
from Server.player import Player
from . import ai_rulebase
from Server.gamestate import GameState
import asyncio
import random
import logging
import copy

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AIStrategy(ABC, GameClient):

    def __init__(self):
        
        self._strength = "Placeholder"
        self._good_luck_message = "Good luck!"
        self._good_game_message_lost = "Good game! You played well."
        self._good_game_message_won = "Good game! I'll have better luck next time."
        self._good_game_message_draw = "Good game! We are evenly matched."
        self._current_uuid = None
        self._rulebase = ai_rulebase.AIRulebase()
        self._ip = "127.0.0.1"
        self._port = 8765

    def post_init(self):
        #needs to be called by inheriting classes at the end of their __init__ function
        super().__init__(self._ip, self._port, self._player)

    def thread_entry(self):
        asyncio.run(self.run())

    async def run(self):

        # The AI-UUID is hardcoded so that it can be excluded from statistics
        await self.join_game()
        asyncio.timeout(1)
        await self.lobby_ready()
        logger.info("test")

        await self._listening_task

    async def join_game(self):
        
        await self.connect()
        self._listening_task = asyncio.create_task(self.listen())
        
        await self.join_lobby()



    async def _message_handler(self, message_type: str):
        
        match message_type:
            case "lobby/status":
                # AI does not need this
                pass
            case "game/start":
                logger.info(f"start {self._starting_player.uuid}")
                if self._starting_player == self._player:
                    await self.do_turn()
                await self.wish_good_luck()
            
            case "game/end":
                await self.say_good_game()
                await self.close()

            case "game/turn":
                if self._current_player == self._player:
                    await self.do_turn()
                
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

    async def wish_good_luck(self):
        await self.chat_message(self._good_luck_message)

    async def say_good_game(self):
        if self._winner.uuid == self._current_uuid:
            await self.chat_message(self._good_game_message_won)
        elif self._winner.uuid == None:
            await self.chat_message(self._good_game_message_draw)
        else:
            await self.chat_message(self._good_game_message_lost)

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
    
    def __init__(self, uuid: str = '108eaa05-2b0e-4e00-a190-8856edcd56a5'):
        super().__init__()
        self._current_uuid = uuid
        self._strength = "Weak"
        self._good_luck_message = "Good luck! I'm still learning so please have mercy on me."
        self._good_game_message_lost = "Good game! I will try to do better next time."
        self._good_game_message_won = "Good game! I can't believe I won!"
        self._good_game_message_draw = "Good game! I' happy I didn't lose."
        self._player = Player(f"{self._strength} AI", random.randint(0, 0xFFFFFF), uuid=self._current_uuid)
        self.post_init()
    
    async def do_turn(self):
        empty_cells = self.get_empty_cells(self._playfield)
        move = random.randint(0, len(empty_cells) - 1)
        await self.game_make_move(empty_cells[move][0], empty_cells[move][1])

class AdvancedAIStrategy(AIStrategy):

    def __init__(self, uuid: str = 'd90397a5-a255-4101-9864-694b43ce8a6c'):
        super().__init__()
        self._current_uuid = uuid
        self._strength = "Advanced"
        self._good_luck_message = "Good luck! I hope you are ready for a challenge."
        self._good_game_message_lost = "Good game! I admire your skills."
        self._good_game_message_won = "Good game! I hope you learned something from me."
        self._good_game_message_draw = "Good game! I hope you are ready for a rematch."
        self._player = Player(f"{self._strength} AI", random.randint(0, 0xFFFFFF), uuid=self._current_uuid)
        self.post_init()

    def check_winning_move(self, empty_cells: list, player: int):
        """
        Check if there is a winning move for the given player.
        """
        
        for possible_move in empty_cells:
            temp_gamestate = GameState()

            # Make deep copy of the game state
            temp_gamestate._playfield = copy.deepcopy(self._playfield)

            temp_gamestate.set_player_position(self._player_number, possible_move)
            self._rulebase.check_win(temp_gamestate)
            if temp_gamestate.winner == player:
                return possible_move
        
        return None

    async def do_turn(self):
        """
        Advanced AI Logic:
        1. Make a move if there is a winning move
        2. Block the opponent if there is a winning move
        3. Make a random move(or maybe more complex logic)
        """

        empty_cells = self.get_empty_cells(self._playfield)

        # Check for own winning move
        if (winning_move:= self.check_winning_move(empty_cells, self._player_number)) != None:
            await self.game_make_move(winning_move[0], winning_move[1])
            return
            
        # Check for opponent winning move
        if (winning_move:= self.check_winning_move(empty_cells, self._opponent_number)) != None:
            await self.game_make_move(winning_move[0], winning_move[1])
            return
            
        # Make a random move
        move = random.randint(0, len(empty_cells) - 1)
        await self.game_make_move(empty_cells[move][0], empty_cells[move][1])
