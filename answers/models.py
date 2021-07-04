from questions.models import Question
from django.db import models
from django.db.models.base import Model
from questions.models import Question

class Answer(models.Model):
    answer = models.TextField(blank=False)
    question = models.ForeignKey(Question,on_delete=models.CASCADE,blank=False)
    is_correct = models.CharField(max_length=1, choices=(('F','False'),('T','True')))

