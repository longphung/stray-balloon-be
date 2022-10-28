import json
import datetime
from django.core.serializers import serialize
import django.db.utils
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from app import models


@sync_to_async
def get_roles(l):
    return list(l)


@database_sync_to_async
def create_session(**kwargs):
    session = models.Session(**kwargs)
    session.save()
    return session.id


@database_sync_to_async
def get_session(**kwargs):
    session = models.Session.objects.filter(**kwargs).first()
    return session


@database_sync_to_async
def update_session(session_id, start_time=None, end_time=None):
    session = models.Session.objects.get(id=session_id)
    if start_time is not None:
        session.start_time = start_time
    if end_time is not None:
        session.end_time = end_time
    session.save()


@database_sync_to_async
def create_session_progress(**kwargs):
    session_progress = models.SessionProgress(**kwargs)
    session_progress.save()
    return session_progress.id


class SessionConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.session_group_name = None
        self.session_name = None

    async def connect(self):
        self.session_name = self.scope["url_route"]["kwargs"]["session_name"]
        self.session_group_name = "session_%s" % self.session_name
        user = self.scope["user"]
        roles = user.groups.values_list('name', flat=True)  # QuerySet Object
        roles_as_list = await get_roles(roles)

        if user.is_anonymous:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(self.session_group_name, self.channel_name)

        await self.accept()
        await self.channel_layer.group_send(
            self.session_group_name,
            {"type": "session_join", "username": user.username, "role": json.dumps(roles_as_list)}
        )
        if 'instructors' in roles_as_list:
            session = await get_session(instructor_id=user.id, start_time__isnull=True, end_time__isnull=True)
            if session is None:
                session_id = await create_session(instructor_id=user)
                session_status = "created"
            else:
                session_id = session.id
                session_status = "in_progress"
            await self.send(json.dumps({
                "type": "session_info_instructor",
                "sessionStatus": session_status,
                "sessionId": session_id
            }))

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
        session_id = text_data_json["session_id"]

        if 'instructors' not in roles_as_list or session_status not in ['started', 'ended']:
            return

        if session_status == 'started':
            await update_session(session_id, start_time=datetime.datetime.now())
            await self.channel_layer.group_send(
                self.session_group_name,
                {
                    "type": "session_update",
                    "session_status": session_status,
                    "username": user.username,
                    "session_id": session_id
                }
            )
        elif session_status == 'ended':
            await update_session(session_id, end_time=datetime.datetime.now())
            await self.channel_layer.group_send(
                self.session_group_name,
                {
                    "type": "session_update",
                    "session_status": session_status,
                    "username": user.username,
                    "session_id": session_id
                }
            )

    # Receive message from room group
    async def session_update(self, event):
        session_status = event["session_status"]
        username = event["username"]
        session_id = event["session_id"]

        curr_user = self.scope["user"]
        roles = curr_user.groups.values_list('name', flat=True)  # QuerySet Object
        roles_as_list = await get_roles(roles)

        if session_status == "started" and 'students' in roles_as_list:
            session = await get_session(id=session_id)
            try:
                session_progress_id = await create_session_progress(
                    student_id=curr_user,
                    session_id=session,
                    attended=True,
                    progress=json.dumps({})
                )
                await self.channel_layer.group_send(
                    self.session_group_name,
                    {
                        "type": "session_progress_started",
                        "session_id": session_id,
                        "session_progress_id": session_progress_id,
                        "student": await sync_to_async(serialize)('json', [curr_user])
                    }
                )
            except django.db.utils.DatabaseError:
                print("nothing")

        # Send session_statusto WebSocket
        await self.send(text_data=json.dumps(
            {
                "type": "session_update",
                "session_status": session_status,
                "username": username,
                "session_id": session_id,
            })
        )

    async def session_join(self, event):
        await self.send(text_data=json.dumps({
            "type": "session_join",
            "role": json.loads(event['role']),
            "username": event['username'],
        }))

    async def session_progress_started(self, event):
        curr_user = self.scope["user"]
        roles = curr_user.groups.values_list('name', flat=True)
        roles_as_list = await get_roles(roles)
        if 'instructors' in roles_as_list:
            student_info = json.loads(event["student"])[0]['fields']
            del student_info['password']
            del student_info['is_superuser']
            del student_info['user_permissions']
            await self.send(text_data=json.dumps({
                "type": "session_progress_started",
                "student": student_info,
                "session_id": event["session_id"],
                "session_progress_id": event["session_progress_id"],
            }))
