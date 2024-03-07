from uuid import UUID
from threading import Thread

from Server.websocket_server import Lobby
from Server.player import Player


def server_start(admin:Player, port:int = 8765):
    lobby = Lobby(admin = admin, port = port)
    lobby.run()

def server_thread(admin:Player, port:int = 8765) -> Thread:
    t = Thread(target=server_start, args=(admin, port))
    t.start()
    return t
