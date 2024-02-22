from game import Game
import asyncio
import websockets
import logging
import json

logger = logging.getLogger()

async def handler(websocket):
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
            case "join":
                pass
            case _:
                await websocket.send("Invalid Message Type")
    

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())

