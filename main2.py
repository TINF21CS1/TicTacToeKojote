from Server.websocket_server import Lobby
from Server.player import Player
from uuid import UUID

if __name__ == "__main__":
    lobby = Lobby(port = 8765, admin = Player(uuid=UUID("c4f0eccd-a6a4-4662-999c-17669bc23d5e"), display_name="admin", color=0xffffff))
    lobby.run()