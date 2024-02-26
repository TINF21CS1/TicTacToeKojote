from __future__ import annotations
import asyncio
from Server.player import Player
from Client.client import *

async def example_handler(client:GameClient, message_type:str):
    """Example handler for the game client. This function is called whenever a message is received from the server.
    
    *** Please do not use any busy waiting or blocking code in this function as it will completely halt the listening. ***

    Use `await my_function()` to call an async function and wait for it to finish. Possible use case: Sending a move to the server.
    Example: await client.game_make_move(0, 0) will send a move to the server and only continue execution after the move was successfully sent.

    Use `my_task = asyncio.create_task(my_function())` to call async functions in the background and continue execution even if it is still running. Await the task execution via `await my_task` to wait for the task to finish. Possible use case: Sending chat messages in the background.
    Example: asyncio.create_task(client.chat_message("Hello World")) will send a chat message in the background and continue execution.
    
    Obviously, you can also use my_function() if it is a synchronous function.
    
    Args:
        client (GameClient): The game client that received the message with all updated information.
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

async def new_server_example():
    # Setting up the game
    player = Player(uuid="c4f0eccd-a6a4-4662-999c-17669bc23d5e", display_name="admin", color=0xffffff)
    client, listening_task, server = await create_game(player, example_handler)

    # Do something with the client
    await client.lobby_ready()
    await client.game_make_move(0, 0)
    await client.chat_message("Hello World")

    # Closing the connection
    await client.close()

    # Wrapping up the listening task and the server thread
    await listening_task
    server.join(timeout=1)

async def client_join_example():
    # Setting up the connection
    player = Player(uuid="c4f0eccd-a6a4-4662-999c-17669bc23d5e", display_name="admin", color=0xffffff)
    client, listening_task = await join_game(player, example_handler, "localhost")

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