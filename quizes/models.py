from django.db import models
from users.models import Users

class Quiz(models.Model):
    created_by = models.ForeignKey(Users,on_delete=models.CASCADE,blank=False)
    name = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now=True)
