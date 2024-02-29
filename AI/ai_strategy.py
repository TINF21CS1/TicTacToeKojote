from abc import ABC, abstractmethod
from Client.client import GameClient
from Server.player import Player
import asyncio
import random

class AIStrategy(ABC, GameClient):

    def __init__(self):
        _strength = "Placeholder"

    def thread_start(self):
        asyncio.run(self.run())

    async def run(self):

        # The AI-UUID is hardcoded so that it can be excluded from statistics
        await self.join_game(Player(f"{self._strength} AI", random.randint(0, 0xFFFFFF)), "127.0.0.1", uuid="108eaa05-2b0e-4e00-a190-8856edcd56a5")
        await self.lobby_ready()


    async def _message_handler(self, message_type: str):
        
        match message_type:
            case "lobby/status":
                # AI does not need this
                pass
            case "game/start":
                self.wish_good_luck()
                pass
            case "game/end":
                self.say_good_game()
                pass
            case "game/turn":
                self.do_turn()
                pass
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

    @abstractmethod
    def wish_good_luck(self):
        pass

    @abstractmethod
    def say_good_game(self):
        pass

    @abstractmethod
    def do_turn(self):
        pass

        

class WeakAIStrategy(AIStrategy):
    
    def __init__(self):
        _strength = "Weak"

    def run(self):
        print("Weak AI placeholder")

class AdvancedAIStrategy(AIStrategy):

    def __init__(self):
        _strength = "Advanced"

    def run(self):
        print("Strong AI placeholder")
