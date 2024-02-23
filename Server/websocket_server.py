from game import Game
from player import Player
from rulebase import RuleBase
import asyncio
import websockets
import logging
import json

logger = logging.getLogger()

class Lobby:
    def __init__(self, admin:Player) -> None:
        self._players = [admin]
        self._readystatus: dict = {admin.id, False}
        self._game = None
        self._inprogress = False
        

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

                    if self._inprogress:
                        await websocket.send("Game in progress, cannot join") # TODO jsonify
                        break

                    self._players.append(Player(message_json["profile"]["id"], message_json["profile"]["display_name"], message_json["profile"]["color"]))
                    self._readystatus[message_json["profile"]["id"]] = False

                    # await websocket.send( ## STATISTICS ## )
                    await websocket.broadcast(json.dumps({
                        "message_type": "lobby/status",
                        "players": self._players,
                        "ready_status": self._readystatus
                    }))
                

                case "lobby/kick":
                    pass
                
                
                case "lobby/ready":

                    self._readystatus[message_json["profile"]["id"]] = True

                    await websocket.broadcast(json.dumps({
                        "message_type": "lobby/status",
                        "players": self._players,
                        "ready_status": self._readystatus
                    }))

                    if all(self._readystatus.values() & len(self._players) == 2):
                        # TODO add error messages for why game cant start with not enough or too many ready players
                        # all players are ready, start the game
                        rulebase = RuleBase()
                        self._game = Game(player1 = self._players[0], player2 = self._players[1], rulebase = rulebase)
                        await websocket.broadcast(json.dumps({
                            "message_type": "game/start",
                            "current_player": self._game.state.current_player,
                        }))
                
                
                case "game/make_move":
                    pass
                
                
                case "chat/message":
                    pass
                
                
                case _:
                    await websocket.send("Invalid Message Type")
        

    async def start_server(self, port: int = 8765):
        async with websockets.serve(self.handler, host = "", port = port):
            await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(Lobby.start_server(port = 8765, admin = Player(0, "admin", 0xffffff)))

