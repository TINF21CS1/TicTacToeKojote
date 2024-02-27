from Server.game import Game
from Server.player import Player
from Server.rulebase import RuleBase
import asyncio
import websockets
import logging
import json
from jsonschema import validate, ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Lobby:
    def __init__(self, admin:Player, port: int = 8765) -> None:
        self._players = {admin.uuid : admin}
        self._game = None
        self._inprogress = False
        self._port = port
        self._connections = set()

        with open("./json_schema/client_to_server.json", "r") as f:
            self._json_schema = json.load(f)

    async def handler(self, websocket):
        
        self._connections.add(websocket)

        while True:
            try:
                message = await websocket.recv()

                logger.info(f"Received: {message}")
            
                message_json = json.loads(message)
                
                # Validate JSON
                try:
                    validate(instance=message_json, schema=self._json_schema)
                except ValidationError as e:
                    logger.error(e)
                    continue

                match message_json["message_type"]:

                    case "lobby/join":

                        if self._inprogress:
                            await websocket.send("Game in progress, cannot join") # TODO jsonify
                            break

                        self._players[message_json["profile"]["uuid"]] = Player(uuid=message_json["profile"]["uuid"], display_name=message_json["profile"]["display_name"], color=message_json["profile"]["color"])

                        # await websocket.send( ## STATISTICS ## )
                        websockets.broadcast(self._connections, json.dumps({
                            "message_type": "lobby/status",
                            "players": [player.__dict__() for player in self._players.values()],
                        }))
                    

                    case "lobby/kick":
                        pass
                    
                    
                    case "lobby/ready":

                        self._players[message_json["player_uuid"]].ready = True

                        websockets.broadcast(self._connections, json.dumps({
                            "message_type": "lobby/status",
                            "players":  [player.__dict__() for player in self._players.values()],
                        }))

                        if all([player.ready for player in self._players.values()]) & len(self._players) == 2:
                            # TODO add error messages for why game cant start with not enough or too many ready players
                            # all players are ready, start the game
                            rulebase = RuleBase()
                            self._game = Game(player1 = self._players.values()[0], player2 = self._players.values()[1], rulebase = rulebase)
                            
                            websockets.broadcast(self._connections, json.dumps({
                                "message_type": "game/start",
                                "starting_player_uuid": self._game.current_player_uuid,
                            }))
                    
                    
                    case "game/make_move":
                        pass
                    
                    
                    case "chat/message":
                        pass
                    
                    
                    case _:
                        await websocket.send("Invalid Message Type")

            except websockets.ConnectionClosedOK:
                logger.info("Connection Closed from Client-Side")
                # TODO: Add handling when game is not over yet
                break
            # TODO: Catch other errors for disconnects
        

    async def start_server(self):
        async with websockets.serve(self.handler, host = "", port = self._port):
            await asyncio.Future()  # run forever

    def run(self):
        asyncio.run(self.start_server())

if __name__ == "__main__":
    lobby = Lobby(port = 8765, admin = Player(uuid="c4f0eccd-a6a4-4662-999c-17669bc23d5e", display_name="admin", color=0xffffff))
    lobby.run()