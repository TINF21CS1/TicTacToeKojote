from __future__ import annotations
import asyncio
from websockets.client import connect
from Server.player import Player
from threading import Thread
from queue import Queue, Empty
import tkinter as tk
from Client.client import GameClient
import logging
from jsonschema import ValidationError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GameClientUI(GameClient):
    """A class to represent a game client that connects to a server and sends and receives messages. This class is specifically designed to be used with a tkinter UI.

    Attributes:
        _tk_root (tk.Tk): The tkinter root window
        _in_queue (Queue): A queue to receive messages from the UI
        _out_queue (Queue): A queue to send messages to the UI

    For the rest of the attributes and methods see the `GameClient` class.
    """

    def __init__(self, ip:str, port:int, player:Player, tk_root:tk.Tk, out_queue:Queue, in_queue:Queue) -> None:
        """Initialize the GameClientUI object.

        Args:
            ip (str): The IP address of the server
            port (int): The port of the server
            player (Player): The player object
            tk_root (tk.Tk): The tkinter root window
            out_queue (Queue): A queue to send messages to the UI
            in_queue (Queue): A queue to receive messages from the UI
        """
        self._tk_root = tk_root
        self._in_queue = in_queue
        self._out_queue = out_queue
        super().__init__(ip, port, player)
    
    @classmethod
    async def join_game(cls, player: Player, ip: str, tk_root:tk.Tk, out_queue:Queue, in_queue:Queue, port: int = 8765) -> GameClientUI:
        """Create a new GameClientUI object and connect to the server.

        Args:
            player (Player): The player object
            ip (str): The IP address of the server
            tk_root (tk.Tk): The tkinter root window
            out_queue (Queue): A queue to send messages to the UI
            in_queue (Queue): A queue to receive messages from the UI
            port (int, optional): The port of the server. Defaults to 8765.

        Returns:
            The GameClientUI object
        """
        
        client = cls(ip, port, player, tk_root, out_queue, in_queue)
        await client.connect()
        await asyncio.create_task(client.join_lobby())
        return client
    
    async def listen(self):
        try:
            async with asyncio.timeout(0.1):
                logger.debug("Waiting for message")
                message = await self._websocket.recv()
        except asyncio.TimeoutError:
            return
        
        logger.info(f"Received: {message}")

        try:
            message_type = await self._preprocess_message(message)
        except ValidationError as e:
            logger.error(e)
            return
        
        await self._message_handler(message_type)
    
    async def _message_handler(self, message_type: str):
        # Receive messages from the server
        match message_type:
            case "lobby/status":
                self._out_queue.put({
                    "message_type": "lobby/status", 
                    "player": self._lobby_status
                })
                self._tk_root.event_generate("<<queue_input>>", when="tail")
            case "game/start":
                self._out_queue.put({
                    "message_type": "game/start",
                    "starting_player": self._current_player,
                    "player1": self._player,
                    "player2": self._opponent,
                    "player1_symbol": self._symbol == "X",
                    "player2_symbol": self._symbol != "X"
                })
                self._tk_root.event_generate("<<queue_input>>", when="tail")
            case "game/end":
                self._out_queue.put({
                    "message_type": "game/end",
                    "winner": self._winner,
                    "win": self._winner == self._player,
                    "final_playfield": self._playfield
                })
                self._tk_root.event_generate("<<queue_input>>", when="tail")
                await self.close()
            case "game/turn":
                self.send_gamestate_to_ui()
            case "game/error":
                self._out_queue.put({
                    "message_type": "game/error",
                    "error_message": self._error_history[-1]
                })
                self._tk_root.event_generate("<<queue_input>>", when="tail")  
            case "chat/receive":
                self._out_queue.put({
                    "message_type": "chat/receive",
                    "sender": self._chat_history[-1][0],
                    "message": self._chat_history[-1][1]
                })
                self._tk_root.event_generate("<<queue_input>>", when="tail")
            case "lobby/kick":
                if self._kicked:
                    self._out_queue.put({
                        "message_type": "lobby/kick",
                    })
                    self._tk_root.event_generate("<<queue_input>>", when="tail")
        return
    
    def send_gamestate_to_ui(self):
        """Send the gamestate to the UI."""
        self._out_queue.put({
            "message_type": "game/turn",
            "next_player": self._current_player.uuid,
            "playfield": self._playfield
        })
        self._tk_root.event_generate("<<queue_input>>", when="tail")
    
    async def await_commands(self):
        """Wait for commands from the UI and send them to the server."""
        try:
            logger.debug("Trying to get message from in_queue")
            message: dict = self._in_queue.get_nowait()
        except Empty:
            await asyncio.sleep(0.1)
            return

        logger.info(f"Sending: {message}")

        if message:
            match message["message_type"]:
                case "lobby/ready":
                    await self.lobby_ready(**message["args"])
                case "lobby/kick":
                    await self.lobby_kick(**message["args"])
                case "game/make_move":
                    await self.game_make_move(**message["args"])
                case "chat/message":
                    await self.chat_message(**message["args"])
                case "server/terminate":
                    await self.terminate()
                case "game/gamestate":
                    self.send_gamestate_to_ui()
                case "statistics/statistics":
                    self._out_queue.put({
                        "message_type": "statistics/statistics",
                        "statistics": self._statistics
                    })
                    self._tk_root.event_generate("<<queue_input>>", when="tail")
                case _:
                    logger.error(f"Unknown message type received from UI in in_queue: {message['message_type']}")
                    return
            
            self._in_queue.task_done()

async def client_thread_function(tk_root:tk.Tk, out_queue:Queue, in_queue:Queue, player: Player, ip:str, port:int) -> None:
    """The function that is run in the client thread. It connects to the server. It sends and receives messages.

    Args:
        tk_root (tk.Tk): The tkinter root window
        out_queue (Queue): A queue to send messages to the UI
        in_queue (Queue): A queue to receive messages from the UI
        player (Player): The player object
        ip (str): The IP address of the server
        port (int): The port of the server
    """

    for _ in range(5):
        try:
            client = await GameClientUI.join_game(player=player, ip=ip, tk_root=tk_root, out_queue=out_queue, in_queue=in_queue, port=port)

            out_queue.put({"message_type": "lobby/connect"})
            tk_root.event_generate("<<queue_input>>", when="tail")

            while client._websocket.open:
                try:
                    await asyncio.create_task(client.listen())
                    await asyncio.create_task(client.await_commands())
                except Exception as e:
                    logger.error(e)
                    out_queue.put({"message_type": "python/error", "error": e})
                    tk_root.event_generate("<<queue_input>>", when="tail")
            break
        
        # If the client is not able to connect to the server, try again
        except Exception as e:
            logger.error(e)
            await asyncio.sleep(1)
    
    # If the client is not able to connect to the server after 5 tries, send an error message to the UI
    out_queue.put({"message_type": "python/error", "error": ConnectionError("Could not connect to server after 5 tries. Please try again later.")})
    tk_root.event_generate("<<queue_input>>", when="tail")

def asyncio_thread_wrapper(tk_root:tk.Tk, out_queue:Queue, in_queue:Queue, player: Player, ip:str, port:int):
    """Wrapper function to run the client thread function in an asyncio event loop.
    
    Args:
        tk_root (tk.Tk): The tkinter root window
        out_queue (Queue): A queue to send messages to the UI
        in_queue (Queue): A queue to receive messages from the UI
        player (Player): The player object
        ip (str): The IP address of the server
        port (int): The port of the server
    """
    asyncio.run(client_thread_function(tk_root, out_queue, in_queue, player, ip, port))

def client_thread(tk_root:tk.Tk, out_queue:Queue, in_queue:Queue, player: Player, ip:str, port:int = 8765) -> Thread:
    """Start a new client thread that connects to the server and sends and receives messages.
    
    Args:
        tk_root (tk.Tk): The tkinter root window
        out_queue (Queue): A queue to send messages to the UI
        in_queue (Queue): A queue to receive messages from the UI
        player (Player): The player object
        ip (str): The IP address of the server
        port (int, optional): The port of the server. Defaults to 8765.
        
    Returns:
        The client thread
    """
    thread = Thread(target=asyncio_thread_wrapper, args=(tk_root, out_queue, in_queue, player, ip , port), daemon=True)
    thread.start()
    return thread