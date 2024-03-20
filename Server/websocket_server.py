from Server.game import Game
from Server.player import Player
from Server.rulebase import RuleBase
from Server.statistics import Statistics

import asyncio
import websockets
import logging
import json
from jsonschema import validate, ValidationError
import uuid
from zeroconf import ServiceInfo, Zeroconf
import socket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Lobby:
    """
    This class represents an instance of the gameserver.

    Parameters:
        admin (Player): The player object of the admin user.
        port (int): The port the server is running on. Default is 8765. (This also shouldnt be changed, since many parts of the client depend on this port.)
    
    Functions:
        handler(websocket) -> None: Handles incoming websocket messages from the client.
        run() -> None: Runs the server async.
    
    Private Functions:
        _end_game() -> None: Ends the game and sends the final playfield and winner to the clients. Then closes the server.
        start_server() -> None: Starts the server.
    """

    def __init__(self, admin:Player, port: int = 8765) -> None:
        self._players = {}
        self._admin = admin
        self._game = None
        self._inprogress = False
        self._port = port
        self._connections = set()
        self._stats = Statistics()

        with open("./json_schema/client_to_server.json", "r") as f:
            self._json_schema = json.load(f)

        # MDNS
        #https://stackoverflow.com/a/74633230
        self._mdns = Zeroconf()
        ip = socket.inet_aton(socket.gethostbyname(socket.gethostname())) # this is a dirty hack and also doesnt work dual stack :'(
        wsInfo = ServiceInfo(type_ = '_tictactoe._tcp.local.', name = admin.display_name+'s-Server'+'._tictactoe._tcp.local.', port = self._port, addresses = [ip])
        self._mdns.register_service(wsInfo)


    async def handler(self, websocket):
        """
        Handle all websocket messages and pass them to the appropriate game function.
        """
        
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

                        self._players[message_json["profile"]["uuid"]] = Player(uuid=uuid.UUID(message_json["profile"]["uuid"]), display_name=message_json["profile"]["display_name"], color=message_json["profile"]["color"])

                        # send new lobby status
                        websockets.broadcast(self._connections, json.dumps({
                            "message_type": "lobby/status",
                            "players": [player.as_dict() for player in self._players.values()],
                        }))

                        # send lobby statistics
                        stats = self._stats.get_statistics()
                        await websocket.send(json.dumps({
                            "message_type": "statistics/statistics",
                            "server_statistics": [
                                {"player": {"uuid": u, "display_name": d, "color": c},"statistics":{"wins": w, "losses": l, "draws": r, "moves": m, "emojis": e}} for (u, d, c, w, l, r, m, e) in stats
                            ],
                        }))


                    case "lobby/kick":
                        websockets.broadcast(self._connections, json.dumps({
                            "message_type": "lobby/kick",
                            "kick_player_uuid": message_json["kick_player_uuid"],
                        }))
 
                    case "lobby/ready":

                        self._players[message_json["player_uuid"]].ready = message_json["ready"]

                        websockets.broadcast(self._connections, json.dumps({
                            "message_type": "lobby/status",
                            "players":  [player.as_dict() for player in self._players.values()],
                        }))

                        if all([player.ready for player in self._players.values()]) and len(self._connections) == 2 and len(self._players) >= 2:
                            # TODO add error messages for why game cant start with not enough or too many ready players
                            # all players are ready, start the game
                            rulebase = RuleBase()
                            self._game = Game(player1 = list(self._players.values())[0], player2 = list(self._players.values())[1], rule_base = rulebase)

                            self._inprogress = True
                            self._mdns.unregister_all_services()
                            
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
                                    self._stats.increment_moves(self._players[message_json["player_uuid"]])
                                except ValueError as e:
                                    await websocket.send(json.dumps({"message_type": "game/error", "error_message": str(e)}))
                                
                                # check for winning state
                                if self._game.state.finished:
                                    await self._end_game()
                                
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
                        self._stats.increment_emojis(self._players[message_json["player_uuid"]], message_json["message"])


                    case "server/terminate":
                        logger.info("Server Termination Requested. Checking if game is in progress.")

                        if self._inprogress:
                            logger.info("Game in progress. Terminating game.")
                            if self._game.players.index(self._players[message_json["player_uuid"]]) == 1:
                                self._game.state.set_winner(2)
                            elif self._game.players.index(self._players[message_json["player_uuid"]]) == 2:
                                self._game.state.set_winner(1)
                            else:
                                self._game.state.set_winner(0)
                            
                            await self._end_game()
                        
                        elif message_json["player_uuid"] == str(self._admin.uuid):
                            # still in lobby, can terminate without game end.
                            logger.info("Not in game. Sender was host. Terminating server.")
                            websockets.broadcast(self._connections, json.dumps({
                                "message_type": "game/error",
                                "error_message": "Server terminated.",
                            }))

                            exit()

                        else:
                            logger.info("Not in game. Sender was not host. Ignoring termination request.")

                    case _:
                        await websocket.send(json.dumps({"message_type": "error", "error": "Unknown message type"}))

            except (websockets.ConnectionClosedOK, websockets.ConnectionClosedError, websockets.ConnectionClosed):
                logger.info("Connection Closed from Client-Side")
                self._connections.remove(websocket)
                if self._inprogress:
                    # connection closed, but not nice. we cannot determine winner, so fuck off
                    self._game.state.set_winner(0)
                    await self._end_game()

                else:
                    # request a ping from everyone and delete player list to wait for join messages.
                    self._players = {}
                    websockets.broadcast(self._connections, json.dumps({
                            "message_type": "lobby/ping",
                        }))

                # End this connection loop
                break

            # TODO: Catch other errors for disconnects
        
    async def _end_game(self):
        self._inprogress = False

        self._stats.increment_games(self._game.players, self._game.state.winner)

        websockets.broadcast(self._connections, json.dumps({
                "message_type": "game/end",
                "winner_uuid": str(self._game.winner.uuid) if self._game.winner else None,
                "final_playfield": self._game.state.playfield,
            }))

        await asyncio.sleep(1)
        exit()

    async def _start_server(self):
        async with websockets.serve(self.handler, host = "", port = self._port):
            await asyncio.Future()  # run forever

    def run(self):
        asyncio.run(self._start_server())

if __name__ == "__main__":
    lobby = Lobby(port = 8765, admin = Player(uuid=uuid.UUID("c4f0eccd-a6a4-4662-999c-17669bc23d5e"), display_name="admin", color=0xffffff, ready=True))
    lobby.run()