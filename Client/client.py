from __future__ import annotations
import asyncio
from websockets.client import connect
import json
from Server.player import Player
import logging
from jsonschema import validate, ValidationError
from uuid import UUID

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GameClient:
    """A class to represent a game client that connects to a server and sends and receives messages.

    Inherit from this class to create your own game client. Overwrite the `_message_handler` method to handle incoming messages from the server your way.
    
    Attributes:
        _ip (str): The IP address of the server.
        _port (int): The port of the server.
        _websocket (WebSocketClientProtocol): The websocket connection to the server.
        _json_schema (dict): The JSON schema to validate incoming messages.
        _player (Player): The player that is using the client.
        _player_number (int): The number of the player in the game. 1 or 2.
        _symbol (str): The symbol of the player in the game. "X" or "O".
        _kicked (bool): Whether the player has been kicked from the lobby.
        _opponent (Player): The opponent of the player.
        _opponent_number (int): The number of the opponent in the game. 1 or 2.
        _starting_player (Player): The player that starts the game.
        _current_player (Player): The player that is currently on turn.
        _lobby_status (list[str]): The status of the lobby.
        _playfield (list[list[int]]): The current playfield of the game.
        _statistics (dict): The statistics of the game.
        _chat_history (list[tuple[Player, str]]): The chat history of the game.
        _winner (Player): The winner of the game.
        _error_history (list[str]): The error history of the game.


    Methods:
        connect: Connect to the server.
        join_game: Join an existing game with the given player.
        listen: Listen for messages from the server.
        get_player_by_uuid: Get a player by its UUID.
        _preprocess_message: Preprocess a message from the server.
        _message_handler: Handle a message from the server.
        join_lobby: Join the lobby of the server.
        lobby_ready: Set the ready status of the player in the lobby.
        lobby_kick: Kick a player from the lobby.
        game_make_move: Make a move in the game.
        chat_message: Send a chat message.
        close: Close the websocket connection. Terminate the thread.
        terminate: Terminate the game.
    """
    
    def __init__(self, ip:str, port:int, player:Player) -> None:
        """Initialize the game client with the given IP, port and player.

        Args:
            ip (str): The IP address of the server.
            port (int): The port of the server.
            player (Player): The player that wants to join the game.
        """
        self._ip: str = ip
        self._port: int = port

        # Player info
        self._player: Player = player
        self._player_number: int = None
        self._symbol: str = None
        self._kicked: bool = False

        # Opponent info
        self._opponent: Player = None
        self._opponent_number: int = None

        # Game info
        self._starting_player: Player = None
        self._current_player: Player = None
        self._lobby_status: list[str] = []
        self._playfield: list[list[int]] = [[0,0,0],[0,0,0],[0,0,0]]
        self._statistics = {}
        self._chat_history: list[tuple[Player, str]] = []
        self._winner: Player = None
        self._error_history: list[str] = []

        with open("./json_schema/server_to_client.json", "r") as f:
            self._json_schema = json.load(f)

    async def connect(self):
        """Connect to the server."""
        # Try 5 times to connect to the server
        for i in range(5):
            try:
                self._websocket = await connect(f"ws://{self._ip}:{str(self._port)}")
                break
            except Exception as e:
                logger.error(f"Could not connect to server. Attempt {i+1}/5. Retrying in 0.5 seconds...")
                await asyncio.sleep(0.5)

    @classmethod
    async def join_game(cls, player: Player, ip:str, port:int = 8765) -> tuple[GameClient, asyncio.Task]:
        """Join an existing game with the given player and message handler.

        This function __has__ to be run in an asyncio event loop. Wrap it in an async function which you then call with `asyncio.run(my_wrapper_function())`. Reminder: `asyncio.run()` can only be called once in a program. Calling `asyncio.run(join_game())` directly will not terminate since the listening task is not awaited.

        Args:
            player (Player): The player that wants to join the game.
            ip (str): The IP address of the server.
            port (int): The port of the server. Default is 8765.

        Returns:
            tuple[GameClient, asyncio.Task]: A tuple containing the game client and the listening task.
        """
        
        client = cls(ip, port, player)
        await client.connect()
        listening_task = asyncio.create_task(client.listen())
        
        await asyncio.create_task(client.join_lobby())

        return client, listening_task

    async def listen(self):
        """Listen for messages from the server."""
        async for message in self._websocket:
            logger.info(f"Received: {message}")

            try:
                message_type = await self._preprocess_message(message)
            except ValidationError as e:
                logger.error(e)
                continue
            
            await self._message_handler(message_type)

            if message_type == "game/end":
                await self.terminate()
                break
            elif self._kicked:
                await self.close()
                break

    def get_player_by_uuid(self, uuid:str) -> Player:
        """Get a player by its UUID.

        Args:
            uuid (str): The UUID of the player.

        Returns:
            Player: The player with the given UUID.
        """
        for player in self._lobby_status:
            if str(player.uuid) == uuid:
                return player
        return None
    
    async def _preprocess_message(self, message:str) -> str:
        """Preprocess a message from the server.

        Args:
            message (str): The message from the server.
        
        Returns:
            str: The type of the message.
        """
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
                logger.info(f"Game ended. Winner: {self._winner.display_name if self._winner else 'Draw'}")
                self._playfield = message_json["final_playfield"]
            case "game/turn":
                self._playfield = message_json["updated_playfield"]
                self._current_player = self.get_player_by_uuid(message_json["next_player_uuid"])
            case "statistics/statistics":
                sorted_statistics = sorted(message_json["server_statistics"], key=lambda x: x["player"]["display_name"])
                for entry in sorted_statistics:
                    self._statistics[Player(**entry["player"])] = entry["statistics"]
            case "game/error":
                self._error_history.append(message_json["error_message"])
                logger.error(f"Game error: {message_json['error_message']}") 
            case "chat/receive":
                sender = self.get_player_by_uuid(message_json["sender_uuid"])
                self._chat_history.append((sender, message_json["message"]))
            case "lobby/ping":
                await self.join_lobby()
            case "lobby/kick":
                if str(self._player.uuid) == message_json["kick_player_uuid"]:
                    logger.info("You have been kicked from the lobby. Closing after processing the message...")
                    self._kicked = True
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
        """Join the lobby of the server."""
        msg = {
                "message_type": "lobby/join",
                "profile": self._player.as_dict()
        }
        await self._websocket.send(json.dumps(msg))

    async def lobby_ready(self, ready:bool = True):
        """Set the ready status of the player in the lobby.

        Args:
            ready (bool, optional): The ready status of the player. Defaults to True.
        """
        msg = {
            "message_type": "lobby/ready",
            "player_uuid": str(self._player.uuid),
            "ready": bool(ready)
        }
        await self._websocket.send(json.dumps(msg))

    async def lobby_kick(self, player_to_kick:UUID):
        """Kick a player from the lobby.

        Args:
            player_to_kick (UUID): The UUID of the player to kick.
        """
        msg = {
            "message_type": "lobby/kick",
            "kick_player_uuid": str(player_to_kick)
        }
        await self._websocket.send(json.dumps(msg))
                                   
    async def game_make_move(self, x:int, y:int):
        """Make a move in the game.

        Args:
            x (int): The x-coordinate of the move.
            y (int): The y-coordinate of the move.
        """
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
        """Send a chat message.

        Args:
            message (str): The message to send.
        """
        msg = {
            "message_type": "chat/message",
            "player_uuid": str(self._player.uuid),
            "message": message
        }
        await self._websocket.send(json.dumps(msg))

    async def close(self):
        """Close the websocket connection. Terminate the thread."""
        await self._websocket.close()
        exit()

    async def terminate(self):
        """Try to terminate the game."""
        msg = {
            "message_type": "server/terminate",
            "player_uuid": str(self._player.uuid)
        }
        await self._websocket.send(json.dumps(msg))
        await asyncio.sleep(0.1)
        if self._websocket.open:
            await self.close()