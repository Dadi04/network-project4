from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    followers = models.JSONField(default=list)
    following = models.JSONField(default=list)

class NewPost(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    text = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(default=timezone.now())
    likes = models.ManyToManyField(User, through='Likes')

class Likes(models.Model):
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who_liked')
    post = models.ForeignKey(NewPost, on_delete=models.CASCADE, related_name='liked_post')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('liked_by', 'post')