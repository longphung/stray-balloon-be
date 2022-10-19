from django.db import models


# Create your models here.
class Question(models.Model):
    description = models.CharField(max_length=65_535)
    level = models.PositiveSmallIntegerField()
    additional_resource = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    feedback = models.CharField(max_length=65_535)


class QuestionAnswer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.RESTRICT)
    description = models.CharField(max_length=65_535)
    is_correct = models.BooleanField()
