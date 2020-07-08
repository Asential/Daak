from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=400)
    likes = models.IntegerField(default=0)
    date = models.DateField(auto_now=False, auto_now_add=True)
    time = models.TimeField(auto_now=False, auto_now_add=True)
    def __str__(self):
        return f"{self.user} : {self.content}"