from django.db import models
from quizes.models import Quiz

class Question(models.Model):
    question = models.TextField(blank=False)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    