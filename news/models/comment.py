from django.db import models

from news.models import User, Post


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    description = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
