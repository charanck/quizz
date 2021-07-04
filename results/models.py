from django.db import models
from users.models import Users
from quizes.models import Quiz

class Result(models.Model):
    attendee = models.ForeignKey(Users,on_delete=models.CASCADE,blank=False)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,blank=False)
    progress = models.CharField(max_length=1, choices=(('C','Completed'),('O','On_Progress')))
    percentage = models.FloatField(default=0.0)
    time_taken = models.CharField(max_length=10)
