# WHY IS THIS VERSION ASYNC?
# Class inherits from AsyncWebsocketConsumer rather than WebsocketConsumer
# All methods are async def rather than just def
# await is used to call asynchronous functions that perform I/O.
# async_to_sync is no longer needed when calling methods on the channel layer.

import json
from typing import Any, Dict, Union
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    """
    A chat consumer class that inherits from AsyncWebsocketConsumer.
    It handles asynchronous WebSocket operations.
    """

    async def connect(self) -> None:
        """
        Handle a new WebSocket connection.
        """
        self.room_name: str = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name: str = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        """
        Handle WebSocket disconnection.

        Args:
            close_code (int): The code for the disconnection.
        """
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data: str) -> None:
        """
        Receive a message from WebSocket.

        Args:
            text_data (str): The received text data in JSON format.
        """
        text_data_json: Dict[str, str] = json.loads(text_data)
        message: str = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    async def chat_message(self, event: Dict[str, Any]) -> None:
        """
        Receive a message from the room group and send it to WebSocket.

        Args:
            event (Dict[str, Any]): The received event from the room group.
        """
        message: Union[str, None] = event.get("message")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
