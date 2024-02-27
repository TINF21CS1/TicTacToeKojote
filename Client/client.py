from __future__ import annotations
import asyncio
from websockets.client import connect
import json
from Server.player import Player
from Server.websocket_server import Lobby
import logging
from jsonschema import validate, ValidationError
from threading import Thread
from queue import Queue
import tkinter as tk

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_game(player: Player, message_handler, port:int = 8765) -> tuple[GameClient, asyncio.Task, Thread]:
    """Start a new game with the given player and message handler. Therefore, create a new server thread and connect to it.

    This function __has__ to be run in an asyncio event loop. Wrap it in an async function which you then call with `asyncio.run(my_wrapper_function())`. Reminder: `asyncio.run()` can only be called once in a program. Calling `asyncio.run(create_game())` directly will not terminate since the server thread is not joined and the listening task is not awaited.

    For an example see `my_example()` and `my_handler()`.
    
    Args:
        player (Player): The player that wants to start a new game.
        message_handler ([type]): The message handler that is called whenever a message is received from the server.
        port (int, optional): The port to start the server on. Defaults to 8765.
    
    Returns:
        GameClient: The game client that is connected to the server and can be used to send messages to the server. (methods are documented in the class itself)
        asyncio.Task: The listening task that listens for messages from the server. It should be awaited at the end of the program.
        Thread: The thread that runs the server. It should be joined at the end of the program.
    """
    
    lobby = Lobby(port = port, admin = player)
    server_thread = Thread(target=lobby.run, daemon=True) # TODO: Maybe remove daemon=True and add a proper shutdown function for database etc.
    server_thread.start()

    client = GameClient("localhost", port, player, message_handler)
    await client.connect()
    listening_task = asyncio.create_task(client.listen())
    await asyncio.create_task(client.join_lobby())

    return client, listening_task, server

async def join_game(player: Player, message_handler, ip:str, port:int = 8765) -> tuple[GameClient, asyncio.Task]:
    """Join an existing game with the given player and message handler.

    This function __has__ to be run in an asyncio event loop. Wrap it in an async function which you then call with `asyncio.run(my_wrapper_function())`. Reminder: `asyncio.run()` can only be called once in a program. Calling `asyncio.run(join_game())` directly will not terminate since the listening task is not awaited.

    For an example see `my_example()` and `my_handler()`.
    
    Args:
        player (Player): The player that wants to join the game.
        message_handler ([type]): The message handler that is called whenever a message is received from the server.
        ip (str): The IP address of the server.
        port (int): The port of the server.
    
    Returns:
        GameClient: The game client that is connected to the server and can be used to send messages to the server. (methods are documented in the class itself)
        asyncio.Task: The listening task that listens for messages from the server. It should be awaited at the end of the program.
    """
    
    client = GameClient(ip, port, player, message_handler)
    await client.connect()
    listening_task = asyncio.create_task(client.listen())
    
    await asyncio.create_task(client.join_lobby())

    return client, listening_task

class GameClient:
    """Represents a client for the game server. It can be used to connect to the server, send messages and listen for messages from the server.

    Args:
        ip (str): The IP address of the server.
        port (int): The port of the server.
        player (Player): The player that wants to connect to the server.
        handler ([type]): The message handler that is called whenever a message is received from the server. See `my_handler` for an example.
        
    Attributes:
        _ip (str): The IP address of the server.
        _port (int): The port of the server.
        _player (Player): The player that wants to connect to the server.
        _handler ([type]): The message handler that is called whenever a message is received from the server.
        _websocket ([type]): The websocket connection to the server.
        _opponent ([type]): The opponent of the player.
        _current_player ([type]): The current player.
        _symbol ([type]): The symbol of the player.
        _lobby_status ([type]): The status of the lobby.
        _game_status ([type]): The status of the game.
        _statistics ([type]): The statistics of the game.
        _chat_history ([type]): The chat history of the game.
        _winner ([type]): The winner of the game.
        _statistics ([type]): The statistics of the game.
        _json_schema ([type]): The JSON schema for the messages from the server.
    """
    
    def __init__(self, ip:str, port:int, player:Player, handler) -> None:
        self._ip: str = ip
        self._port: int = port
        self._handler: function = handler

        # Player info
        self._player: Player = player
        self._player_number: int = None
        self._symbol: str = None

        # Opponent info
        self._opponent: Player = None
        self._opponent_number: int = None

        # Game info
        self._current_player: Player = None
        self._lobby_status: list = []
        self._game_status: list[list[int]] = [[0,0,0],[0,0,0],[0,0,0]]
        self._statistics = None # TODO
        self._chat_history: list[str] = []
        self._winner: Player = None

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
                case "game/start":
                    if len(self._lobby_status) != 2:
                        logger.error("Game start message received, but lobby does not contain 2 players. This should not happen and should be investigated.")
                        continue

                    self._opponent = self._lobby_status[0] if self._lobby_status[0]["uuid"] != str(self._player.uuid) else self._lobby_status[1]

                    if str(self._player.uuid) == message_json["starting_player_uuid"]:
                        self._current_player = self._player  
                        self._symbol = "X"
                        self._player_number = 1
                        self._opponent_number = 2
                    else:
                        self._current_player = self._opponent
                        self._symbol = "O"
                        self._opponent_number = 1
                        self._player_number = 2
                case "game/end":
                    self._winner = self.get_player_by_uuid(message_json["winner_uuid"])
                    self._game_status = message_json["final_playfield"]
                case "game/turn":
                    self._game_status = message_json["updated_playfield"]
                    self._current_player = self.get_player_by_uuid(message_json["next_player_uuid"])
                case "statistics/statistics":
                    # TODO: Add statistics handling
                    pass
                case "game/error":
                    logger.error(f"Game error: {message_json['error_message']}") 
                case "chat/receive":
                    sender = self.get_player_by_uuid(message_json["sender_uuid"])
                    self._chat_history.append((sender, message_json["message"]))
                case _:
                    logger.error(f"Unknown message type: {message_json['message_type']}")
                    continue
            
            await self._handler(self, message_json["message_type"])

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

    async def lobby_kick(self, player_to_kick_index:int):
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

def client_thread(tk_root:tk.Tk, in_queue:Queue, out_queue:Queue, player: Player, ip:str, port:int = 8765) -> Thread:
    thread = Thread(target=client_thread_function, args=(tk_root, in_queue, out_queue), daemon=True)
    thread.start()
    return thread

    # Tkinter Event: <<input>>
    out_queue.put(("game/turn", {}))
    tk_root.event_generate("<<server_message_received>>", when="tail")

    match message_type:
        case "lobby/status":
            # -> [Player]
            pass
        case "game/start":
            # starting_player: Player
            # starting_player_symbol: bool (True = X, False = O)
            # opponent: Player
            # opponent_symbol: bool (True = X, False = O)
            pass
        case "game/end":
            # winner: Player | None
            # final_playfield: [[int]] (1 = O, 2 = X, 0 = empty)
            client.close()
            return
            pass
        case "game/turn":
            # next_player: Player
            # playfield: [[int]] (1 = O, 2 = X, 0 = empty)
            pass
        case "statistics/statistics":
            pass
        case "game/error":
            # error_message: str
            pass
        case "chat/receive":
            # sender: Player
            # message: str
            pass
    return

    return thread