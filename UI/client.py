#!/usr/bin/env python

import asyncio
from websockets.client import connect
import websockets
import json
from Server.player import Player
import logging
from jsonschema import validate, ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def new_game():
    # TODO: Add method to start a new websocket server
    pass

class GameClient:
    def __init__(self, ip:str, port:int, player:Player) -> None:
        self._ip = ip
        self._port = port
        self._player = player

        self._opponent = None
        self._current_player = None
        self._symbol = None

        self._lobby_status = []
        self._game_status = [[0,0,0],[0,0,0],[0,0,0]]
        self._statistics = None
        self.chat_history = []
        self.winner = None

        with open("./json_schema/server_to_client.json", "r") as f:
            self._json_schema = json.load(f)

    async def connect(self):
        self._websocket = await connect(f"ws://{self._ip}:{str(self._port)}")

    async def listen(self):
        async for message in self._websocket:
            logger.info(f"Received: {message}")

            message_json = json.loads(message)
            
            try:
                validate(instance=message_json, schema=self._json_schema)
            except ValidationError as e:
                logger.error(e)
                continue

            match message_json["message_type"]:
                case "lobby/status":
                    self._lobby_status = message_json["players"]
                    
                    # TODO: Add Handler to update UI
                
                case "game/start":
                    if len(self._lobby_status) != 2:
                        logger.error("Game start message received, but lobby does not contain 2 players. This should not happen and should be investigated.")
                        continue

                    self._opponent = self._lobby_status[0] if self._lobby_status[0]["uuid"] != str(self._player.uuid) else self._lobby_status[1]

                    if str(self._player.uuid) == message_json["starting_player_uuid"]:
                        self._current_player = self._player  
                        self._symbol = "X"
                    else:
                        self._current_player = self._opponent
                        self._symbol = "O"

                    # TODO: Add Handler to update UI
                
                case "game/end":
                    self._winner = self.get_player_by_uuid(message_json["winner_uuid"])

                    self._game_status = message_json["final_playfield"]

                    # TODO: Add Handler to update UI

                    break # Game ended, no need to continue listening
                
                case "game/turn":
                    self._game_status = message_json["updated_playfield"]

                    self._current_player = self.get_player_by_uuid(message_json["next_player_uuid"])

                    # TODO: Add Handler to update UI
                
                case "statistics/statistics":
                    # TODO: Add Handler to update UI
                    pass
                
                case "game/error":
                    logger.error(f"Game error: {message_json['error_message']}") 
                    # TODO: Add Handler to update UI
                
                case "chat/receive":

                    sender = self.get_player_by_uuid(message_json["sender_uuid"])
                    self.chat_history.append((sender, message_json["message"]))

                    # TODO: Add Handler to update UI

                case _:
                    logger.error(f"Unknown message type: {message_json['message_type']}")
                    continue

    def get_player_by_uuid(self, uuid:str):
        for player in self._lobby_status:
            if player["uuid"] == uuid:
                return player
        return None

    async def join_lobby(self):
        msg = {
                "message_type": "lobby/join",
                "profile": self._player.__dict__()
        }
        await self._websocket.send(json.dumps(msg))

    async def lobby_ready(self):
        msg = {
            "message_type": "lobby/ready",
            "player_uuid": str(self._player.uuid),
            "ready": True
        }
        await self._websocket.send(json.dumps(msg))

    async def lobby_kick(self, player_to_kick:Player):
        msg = {
            "message_type": "lobby/kick",
            "admin_player_uuid": str(self._player.uuid),
            "kick_player_uuid": str(player_to_kick.uuid)
        }
        await self._websocket.send(json.dumps(msg))
                                   
    async def game_make_move(self, x:int, y:int):
        msg = {
            "message_type": "game/make_move",
            "player_uuid": str(self._player.uuid),
            "move": {
                "x": x,
                "y": y
            }
        }
        await self._websocket.send(json.dumps(msg))

    async def chat_message(self, message:str):
        msg = {
            "message_type": "chat/message",
            "player_uuid": str(self._player.uuid),
            "message": message
        }
        await self._websocket.send(json.dumps(msg))

    async def close(self):
        await self._websocket.close()

async def test():
    player = Player("test", 1, "c4f0eccd-a6a4-4662-999c-17669bc23d5e")
    client = GameClient("127.0.0.1", 8765, player)
    await client.connect()
    listening_task = asyncio.create_task(client.listen())
    
    await asyncio.create_task(client.join_lobby())
    asyncio.create_task(client.lobby_ready()) 
    asyncio.create_task(client.lobby_kick(player))
    asyncio.create_task(client.game_make_move(1, 1))
    asyncio.create_task(client.chat_message("Hello World"))
    
    await asyncio.sleep(5)

    await client.close()

if __name__ == "__main__":
    asyncio.run(test())