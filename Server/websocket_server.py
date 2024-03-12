from Server.game import Game
from Server.player import Player
from Server.rulebase import RuleBase
import asyncio
import websockets
import logging
import json
from jsonschema import validate, ValidationError
from uuid import UUID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Lobby:
    def __init__(self, admin:Player, port: int = 8765) -> None:
        self._players = {}
        #self._players = {admin.uuid : admin}
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

                        self._players[message_json["profile"]["uuid"]] = Player(uuid=UUID(message_json["profile"]["uuid"]), display_name=message_json["profile"]["display_name"], color=message_json["profile"]["color"])

                        websockets.broadcast(self._connections, json.dumps({
                            "message_type": "lobby/status",
                            "players": [player.as_dict() for player in self._players.values()],
                        }))


                    case "lobby/kick":
                        pass

 
                    case "lobby/ready":

                        self._players[message_json["player_uuid"]].ready = True

                        websockets.broadcast(self._connections, json.dumps({
                            "message_type": "lobby/status",
                            "players":  [player.as_dict() for player in self._players.values()],
                        }))

                        if all([player.ready for player in self._players.values()]) and len(self._connections) == 2:
                            # TODO add error messages for why game cant start with not enough or too many ready players
                            # all players are ready, start the game
                            rulebase = RuleBase()
                            self._game = Game(player1 = list(self._players.values())[0], player2 = list(self._players.values())[1], rule_base = rulebase)

                            self._inprogress = True
                            
                            websockets.broadcast(self._connections, json.dumps({
                                "message_type": "game/start",
                                "starting_player_uuid": self._game.current_player_uuid,
                            }))


                    case "game/make_move":
                        # check if move can be made
                        if not self._inprogress:
                            await websocket.send(json.dumps({"message_type": "game/error", "error_message": "Game not in progress"}))
                        else:
                            if message_json["player_uuid"] != self._game.current_player_uuid:
                                await websocket.send(json.dumps({"message_type": "game/error", "error_message": "Not your turn"}))
                            else:

                                # make move, catch illegal move
                                try:
                                    self._game.move(self._game.players.index(self._players[message_json["player_uuid"]]), (message_json["move"]["x"], message_json["move"]["y"]))
                                except ValueError as e:
                                    await websocket.send(json.dumps({"message_type": "game/error", "error_message": str(e)}))
                                
                                # check for winning state
                                if self._game.state.finished:
                                    websockets.broadcast(self._connections, json.dumps({
                                        "message_type": "game/end",
                                        "winner_uuid": self._game.state.winner.uuid,
                                        "final_playfiled": self._game.state.playfield,
                                    }))
                                    self._inprogress = False
                                
                                # announce new game state
                                else:
                                    websockets.broadcast(self._connections, json.dumps({
                                        "message_type": "game/turn",
                                        "updated_playfield": self._game.state.playfield,
                                        "next_player_uuid": self._game.current_player_uuid,
                                    }))


                    case "chat/message":
                        websockets.broadcast(self._connections, json.dumps({
                            "message_type": "chat/receive",
                            "sender_uuid": message_json["player_uuid"],
                            "message": message_json["message"],
                        }))


                    case _:
                        await websocket.send(json.dumps({"message_type": "error", "error": "Unknown message type"}))

            except (websockets.ConnectionClosedOK, websockets.ConnectionClosedError, websockets.ConnectionClosed):
                logger.info("Connection Closed from Client-Side")
                self._connections.remove(websocket)
                # TODO: Add handling when game is not over yet
                break
            # TODO: Catch other errors for disconnects
        

    async def start_server(self):
        async with websockets.serve(self.handler, host = "", port = self._port):
            await asyncio.Future()  # run forever

    def run(self):
        asyncio.run(self.start_server())

if __name__ == "__main__":
    lobby = Lobby(port = 8765, admin = Player(uuid=UUID("c4f0eccd-a6a4-4662-999c-17669bc23d5e"), display_name="admin", color=0xffffff, ready=True))
    lobby.run()