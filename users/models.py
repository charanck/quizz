from django.db import models
from django.contrib.auth.models import User


class Users(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,unique=True,blank=False)
    role = models.CharField(max_length=1, choices=(('S','student'),('T','teacher'),('A','Admin')))

    def __str__(self):
        return self.role
