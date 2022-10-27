import json
from django.contrib.auth.models import User
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

from app import models


class QuestionsConsumer(JsonWebsocketConsumer):
    groups = ["broadcast"]

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.session_group_name = None
        self.session_name = None

    def connect(self):
        self.session_name = self.scope["url_route"]["kwargs"]["session_name"]
        self.session_group_name = "session_%s" % self.session_name
        # Join room group
        await self.channel_layer.group_add(self.session_group_name, self.channel_name)
        # Called on connection.
        # To accept the connection call:
        self.accept()

    def receive_json(self, content):
        user = self.scope["user"]
        roles = user.groups.values_list('name', flat=True)
        roles_as_list = list(roles)
        if 'students' not in roles_as_list:
            return
        session_progress = models.SessionProgress(id=content.session_progress_id)
        session_progress.progress = json.dumps({
            "question_id": content.question_id,
            "question_status": content.question_status,
            "answer_taken": content.answer_taken,
            "time_taken": content.time_taken,
        })
        session_progress.save()
        async_to_sync(self.channel_layer.group_send)(
            self.session_group_name,
            {
                "type": "question_answered",
                "student_id": user.id,
                "session_progress": json.dumps(session_progress.progress)
            }
        )

    def disconnect(self, close_code):
        # Called when the socket closes
        await self.channel_layer.group_discard(self.session_group_name, self.channel_name)

    def question_answered(self, event):
        student_id = event["student_id"]
        session_progress = json.loads(event["session_progress"])
        student = User.objects.filter(id=student_id)

        self.send_json(content={
            "student": student,
            "session_progress": session_progress
        })
