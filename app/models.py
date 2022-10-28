from django.db import models
from django.contrib.auth.models import User


class ClassRoom(models.Model):
    class_name = models.CharField(max_length=255)
    year_level = models.PositiveSmallIntegerField()
    instructor = models.ForeignKey(User, on_delete=models.RESTRICT)


class ClassRoomStudents(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    class_room_id = models.ForeignKey(ClassRoom, on_delete=models.RESTRICT)

    class Meta:
        unique_together = (('student_id', 'class_room_id'),)


# Question descriptions and data
class Question(models.Model):
    description = models.CharField(max_length=65_535)
    level = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=255)
    feedback = models.CharField(max_length=65_535, blank=True)


# Multiple selection answers for each session
class QuestionAnswer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.RESTRICT)
    description = models.CharField(max_length=65_535)
    is_correct = models.BooleanField()


class Session(models.Model):
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)
    instructor_id = models.ForeignKey(User, on_delete=models.RESTRICT)


class SessionsQuestions(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.RESTRICT)
    question_id = models.ForeignKey(Question, on_delete=models.RESTRICT)

    class Meta:
        unique_together = (('session_id', 'question_id'),)


class SessionProgress(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    session_id = models.ForeignKey(Session, on_delete=models.RESTRICT)
    attended = models.BooleanField()
    '''
    Progress is an array with each item having the shape of:
    {
        question_id,
        question_status,
        answer_taken,
        time_taken
    }
    question_status is straightforward

    answer_taken can be used to determine whether it was correct or not,
    hence storing a correct field is redundant and provides less data than storing answer_taken

    time_taken is the time taken for that individual question
    '''
    progress = models.JSONField()

    class Meta:
        unique_together = (('student_id', 'session_id'),)
