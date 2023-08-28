from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.views.generic import ListView

class User(AbstractUser):
    followers = models.JSONField(default=list)
    following = models.JSONField(default=list)

class NewPost(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    text = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
