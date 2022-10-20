from django.db import models
from django.contrib.auth.models import User


class ClassRoom(models.Model):
    class_name = models.CharField(max_length=255)
    year_level = models.PositiveSmallIntegerField()
    instructor = models.ForeignKey(User, on_delete=models.RESTRICT)


class ClassRoomStudents(models.Model):
    student_ids = models.ForeignKey(User, on_delete=models.RESTRICT)
    class_room_ids = models.ForeignKey(ClassRoom, on_delete=models.RESTRICT)

    class Meta:
        unique_together = (('student_ids', 'class_room_ids'),)


# Question descriptions and data
class Question(models.Model):
    description = models.CharField(max_length=65_535)
    level = models.PositiveSmallIntegerField()
    additional_resource = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    feedback = models.CharField(max_length=65_535)


# Multiple selection answers for each session
class QuestionAnswer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.RESTRICT)
    description = models.CharField(max_length=65_535)
    is_correct = models.BooleanField()


class Session(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    instructor_id = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='instructor')
    questions = models.ForeignKey(Question, on_delete=models.RESTRICT)


class SessionProgress(models.Model):
    student_ids = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='students')
    session_id = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='session')

    class Meta:
        unique_together = (('student_ids', 'session_id'),)
