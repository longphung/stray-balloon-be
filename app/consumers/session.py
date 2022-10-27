import json
from asgiref.sync import sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer


@sync_to_async
def get_roles(l):
    return list(l)


class SessionConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.session_group_name = None
        self.session_name = None

    async def connect(self):
        self.session_name = self.scope["url_route"]["kwargs"]["session_name"]
        self.session_group_name = "session_%s" % self.session_name
        user = self.scope["user"]
        l = user.groups.values_list('name', flat=True)  # QuerySet Object
        l_as_list = await get_roles(l)

        # Join room group
        await self.channel_layer.group_add(self.session_group_name, self.channel_name)

        await self.accept()
        await self.channel_layer.group_send(
            self.session_group_name, {"type": "session_join", "username": user.username, "role": json.dumps(l_as_list)}
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.session_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        # session_status can be "started" or "ended"
        text_data_json = json.loads(text_data)
        session_status = text_data_json["session_status"]
        user = self.scope["user"]
        roles_list = user.groups.values_list('name', flat=True)  # QuerySet Object
        roles_as_list = await get_roles(roles_list)
        if 'instructors' not in roles_as_list or session_status not in ['started', 'ended']:
            return
        # Send message to room group
        await self.channel_layer.group_send(
            self.session_group_name,
            {
                "type": "session_start",
                "session_status": session_status,
                "username": user.username
            }
        )

    # Receive message from room group
    async def session_start(self, event):
        session_status = event["session_status"]
        username = event["username"]

        # Send session_statusto WebSocket
        await self.send(text_data=json.dumps(
            {
                "session_status": session_status,
                "username": username
            })
        )

    async def session_join(self, event):
        await self.send(text_data=json.dumps({
            "role": event['role'],
            "username": event['username']
        }))
