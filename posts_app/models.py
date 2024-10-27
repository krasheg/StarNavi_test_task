from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
class CustomUser(AbstractUser):
    """Add AI response permission for user model"""
    autoreply = models.BooleanField(default=False)
    autoreply_delay = models.PositiveSmallIntegerField(default=10)


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    blocked = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    blocked = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def to_json(self):
        result = {
            'id': self.id,
            'author': self.author.pk,
            'content': self.content,
            'date_posted': self.date_posted,
            'answers': []
        }
        if self.parent:
            result.update({'parent': self.parent.pk})
        else:
            result.update({'parent': None})
        return result

    def __str__(self):
        return self.content
