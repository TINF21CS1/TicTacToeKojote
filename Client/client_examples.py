from __future__ import annotations
import asyncio
from Server.player import Player
from Client.client import *
from uuid import UUID

async def client_join_example():
    # Setting up the connection
    player = Player(uuid=UUID("c4f0eccd-a6a4-4662-999c-17669bc23d5e"), display_name="admin", color=0xffffff)
    client, listening_task = await GameClient.join_game(player, "localhost")

    # Do something with the client
    await client.lobby_ready()
    await client.game_make_move(0, 0)
    await client.chat_message("Hello World")

    # Closing the connection
    await client.close()

    # Wrapping up the listening task
    await listening_task

if __name__ == "__main__":
    asyncio.run(client_join_example())