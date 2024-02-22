#!/usr/bin/env python

import asyncio
from websockets.sync.client import connect
import json

def hello():
    with connect("ws://localhost:8001") as websocket:

        obj = {
            "message_type": "asdf",
            "username": "my_username"
        }

        websocket.send(json.dumps(obj))
        message = websocket.recv()
        print(f"Received: {message}")

hello()
