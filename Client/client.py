from __future__ import annotations
import asyncio
from websockets.client import connect
import json
from Server.player import Player
from Server.websocket_server import Lobby
import logging
from jsonschema import validate, ValidationError
from threading import Thread
from uuid import UUID

# Set up logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class GameClient:
    """A class to represent a game client that connects to a server and sends and receives messages.

    Inherit from this class to create your own game client. Overwrite the `_message_handler` method to handle incoming messages from the server your way.
    
    Attributes:
        _ip (str): The IP address of the server.
        _port (int): The port of the server.
        _player (Player): The player that is using the client.
        _player_number (int): The number of the player in the game. 1 for the first player, 2 for the second player.
        _symbol (str): The symbol of the player in the game. "X" for the first player, "O" for the second player.
        _opponent (Player): The opponent of the player in the game.
        _opponent_number (int): The number of the opponent in the game. 1 for the first player, 2 for the second player.
        _current_player (Player): The player that is currently allowed to make a move.
        _lobby_status (list[str]): The status of the lobby. Contains all players in the lobby.
        _playfield (list[list[int]]): The status of the game. Contains the current playfield.
        _statistics: The statistics of the game. TODO
        _chat_history (list[tuple[Player, str]]): The chat history of the game. Contains all messages sent in the game.
        _winner (Player): The winner of the game. None if the game is not finished yet or it is a draw.
        _error_history (list[str]): The error history of the game. Contains all errors that occurred for this client.
        _json_schema (dict): The JSON schema that is used to validate incoming messages.
        _websocket: The websocket connection to the server.

    Methods:
        connect: Connect to the server. (This should not be called directly, use `create_game` or `join_game` instead.)
        create_game: Create a new game with the given player. 
        join_game: Join an existing game with the given player.
        listen: Listen for messages from the server. (This should not be called directly, use `create_game` or `join_game` instead.)
        get_player_by_uuid: Get a player by its UUID. 
        join_lobby: Join the lobby of the server.
        lobby_ready: Set the player ready in the lobby.
        lobby_kick: Kick a player from the lobby. (Only the admin can do this.)
        game_make_move: Make a move in the game.
        chat_message: Send a chat message.
        close: Close the connection to the server.
    """
    
    def __init__(self, ip:str, port:int, player:Player) -> None:
        self._ip: str = ip
        self._port: int = port

        # Player info
        self._player: Player = player
        self._player_number: int = None
        self._symbol: str = None

        # Opponent info
        self._opponent: Player = None
        self._opponent_number: int = None

        # Game info
        self._starting_player: Player = None
        self._current_player: Player = None
        self._lobby_status: list[str] = []
        self._playfield: list[list[int]] = [[0,0,0],[0,0,0],[0,0,0]]
        self._statistics = None # TODO
        self._chat_history: list[tuple[Player, str]] = []
        self._winner: Player = None
        self._error_history: list[str] = []

        with open("./json_schema/server_to_client.json", "r") as f:
            self._json_schema = json.load(f)

    async def connect(self):
        self._websocket = await connect(f"ws://{self._ip}:{str(self._port)}")

    @classmethod
    async def create_game(cls, player: Player, port:int = 8765) -> tuple[GameClient, asyncio.Task, Thread]:
        """Start a new game with the given player. Therefore, create a new server thread and connect to it.

        This function __has__ to be run in an asyncio event loop. Wrap it in an async function which you then call with `asyncio.run(my_wrapper_function())`. Reminder: `asyncio.run()` can only be called once in a program. Calling `asyncio.run(GameClient.create_game())` directly will not terminate since the server thread is not joined and the listening task is not awaited.

        For an example see `my_example()` and `my_handler()`.
        
        Args:
            player (Player): The player that wants to start a new game.
            port (int, optional): The port to start the server on. Defaults to 8765.
        
        Returns:
            GameClient: The game client that is connected to the server and can be used to send messages to the server. (methods are documented in the class itself)
            asyncio.Task: The listening task that listens for messages from the server. It should be awaited at the end of the program.
            Thread: The thread that runs the server. It should be joined at the end of the program.
        """
        
        lobby = Lobby(port = port, admin = player)
        server_thread = Thread(target=lobby.run, daemon=True) # TODO: Maybe remove daemon=True and add a proper shutdown function for database etc.
        server_thread.start()

        client = cls("localhost", port, player)
        await client.connect()
        listening_task = asyncio.create_task(client.listen())
        await asyncio.create_task(client.join_lobby())

        return client, listening_task, server_thread

    @classmethod
    async def join_game(cls, player: Player, ip:str, port:int = 8765) -> tuple[GameClient, asyncio.Task]:
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
        
        client = cls(ip, port, player)
        await client.connect()
        listening_task = asyncio.create_task(client.listen())
        
        await asyncio.create_task(client.join_lobby())

        return client, listening_task

    async def listen(self):
        async for message in self._websocket:
            logger.info(f"Received: {message}")

            try:
                message_type = await self._preprocess_message(message)
            except ValidationError as e:
                logger.error(e)
                continue
            
            await self._message_handler(message_type)

    def get_player_by_uuid(self, uuid:str) -> Player:
        for player in self._lobby_status:
            if str(player.uuid) == uuid:
                return player
        return None
    
    async def _preprocess_message(self, message:str) -> str:
            message_json = json.loads(message)
            
            try:
                validate(instance=message_json, schema=self._json_schema)
            except ValidationError as e:
                logger.error(e)
                raise ValidationError(e)

            match message_json["message_type"]:
                case "lobby/status":
                    self._lobby_status = [Player.from_dict(player_dict) for player_dict in message_json["players"]]
                case "game/start":
                    if len(self._lobby_status) != 2:
                        logger.error("Game start message received, but lobby does not contain 2 players. This should not happen and should be investigated.")
                        raise ValidationError("Game start message received, but lobby does not contain 2 players. This should not happen and should be investigated.")


                    self._opponent = self._lobby_status[0] if self._lobby_status[0] != self._player else self._lobby_status[1]

                    if self._opponent == self._player:
                        logger.error("player and opponent are equal")


                    if str(self._player.uuid) == message_json["starting_player_uuid"]:
                        self._current_player = self._player
                        self._starting_player = self._player
                        self._symbol = "X"
                        self._player_number = 1
                        self._opponent_number = 2
                    else:
                        self._current_player = self._opponent
                        self._starting_player = self._opponent
                        self._symbol = "O"
                        self._opponent_number = 1
                        self._player_number = 2
                case "game/end":
                    self._winner = self.get_player_by_uuid(message_json["winner_uuid"])
                    self._playfield = message_json["final_playfield"]
                case "game/turn":
                    self._playfield = message_json["updated_playfield"]
                    self._current_player = self.get_player_by_uuid(message_json["next_player_uuid"])
                case "statistics/statistics":
                    # TODO: Add statistics handling
                    pass
                case "game/error":
                    self._error_history.append(message_json["error_message"])
                    logger.error(f"Game error: {message_json['error_message']}") 
                case "chat/receive":
                    sender = self.get_player_by_uuid(message_json["sender_uuid"])
                    self._chat_history.append((sender, message_json["message"]))
                case _:
                    logger.error(f"Unknown message type: {message_json['message_type']}")
                    raise ValidationError("Game start message received, but lobby does not contain 2 players. This should not happen and should be investigated.")
                
            return message_json["message_type"]

    async def _message_handler(self, message_type:str):
        """Example handler for the game client. This function is called whenever a message is received from the server.
        
        *** Please do not use any busy waiting or blocking code in this function as it will completely halt the listening. ***

        Use `await my_function()` to call an async function and wait for it to finish. Possible use case: Sending a move to the server.
        Example: await client.game_make_move(0, 0) will send a move to the server and only continue execution after the move was successfully sent.

        Use `my_task = asyncio.create_task(my_function())` to call async functions in the background and continue execution even if it is still running. Await the task execution via `await my_task` to wait for the task to finish. Possible use case: Sending chat messages in the background.
        Example: asyncio.create_task(client.chat_message("Hello World")) will send a chat message in the background and continue execution.
        
        Obviously, you can also use my_function() if it is a synchronous function.
        
        Args:
            self (GameClient): The game client that received the message with all updated information.
            message_type (str): The type of the message received.
        
        Returns:
            None    
        """

        match message_type:
            case "lobby/status":
                pass
            case "game/start":
                pass
            case "game/end":
                pass
            case "game/turn":
                pass
            case "statistics/statistics":
                pass
            case "game/error":
                pass
            case "chat/receive":
                pass
        return

    async def join_lobby(self):
        msg = {
                "message_type": "lobby/join",
                "profile": self._player.as_dict()
        }
        await self._websocket.send(json.dumps(msg))

    async def lobby_ready(self, ready:bool = True):
        msg = {
            "message_type": "lobby/ready",
            "player_uuid": str(self._player.uuid),
            "ready": bool(ready)
        }
        await self._websocket.send(json.dumps(msg))

    async def lobby_kick(self, player_to_kick:UUID):
        msg = {
            "message_type": "lobby/kick",
            "admin_player_uuid": str(self._player.uuid),
            "kick_player_uuid": str(player_to_kick)
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