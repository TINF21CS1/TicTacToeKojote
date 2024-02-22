from game import Game
from player import Player
import asyncio
import websockets
import logging
import json

logger = logging.getLogger()

class Lobby:
    def __init__(self, admin:Player) -> None:
        self._players = [admin]
        

    async def handler(self, websocket):
        while True:
            try:
                message = await websocket.recv()
            except websockets.ConnectionClosedOK:
                logger.info("Connection Closed from Client-Side")
                # TODO: Add handling when game is not over yet
                break
            
            # TODO: Catch other errors for disconnects

            logger.info(f"Received: {message}")
            
            message_json = json.loads(message)
            match message_json["message_type"]:
                case "lobby/join":
                    Player(1, message_json["player"]["display_name"])
                case "lobby/ready":
                    pass
                case "game/make_move":
                    pass
                case "chat/message":
                    pass
                case _:
                    await websocket.send("Invalid Message Type")
        

    async def start_server(self, port: int = 8765):
        async with websockets.serve(self.handler, "", port):
            await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(Lobby.start_server(port = 8765, admin = Player(0, "admin")))

