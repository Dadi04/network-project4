from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    follows = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)

class NewPost(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    text = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)