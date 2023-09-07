import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        """
        Obtains the 'room_name' parameter from the URL route in chat/routing.py that opened the WebSocket connection to the consumer.
        Every consumer has a scope that contains information about its connection, including in particular any positional or keyword arguments from the URL route and the currently authenticated user if any.
        """
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
        """
        Constructs a Channels group name directly from the user-specified room name, without any quoting or escaping.
        Group names may only contain alphanumerics, hyphens, underscores, or periods. Therefore this example code will fail on room names that have other characters.
        """
        self.room_group_name = f"chat_{self.room_name}"

        """
        Join a room group.
        The async_to_sync(...) wrapper is required because ChatConsumer is a synchronous WebsocketConsumer but it is calling an asynchronous channel layer method. (All channel layer methods are asynchronous.)
        Group names are restricted to ASCII alphanumerics, hyphens, and periods only and are limited to a maximum length of 100 in the default backend. Since this code constructs a group name directly from the room name, it will fail if the room name contains any characters that aren’t valid in a group name or exceeds the length limit.
        """
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        """
        Accepts the WebSocket connection.
        If you do not call accept() within the connect() method then the connection will be rejected and closed. You might want to reject a connection for example because the requesting user is not authorized to perform the requested action.
        It is recommended that accept() be called as the last action in connect() if you choose to accept the connection.
        """
        self.accept()

    def disconnect(self, close_code):
        # Leave a room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        """
        Sends an event to a group.
        An event has a special 'type' key corresponding to the name of the method that should be invoked on consumers that receive the event. This translation is done by replacing . with _, thus in this example, chat.message calls the chat_message method.
        """
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {"type": "chat.message", "message": message})

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))