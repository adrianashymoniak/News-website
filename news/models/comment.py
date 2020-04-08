from django.db import models
from froala_editor.widgets import FroalaEditor

from news.models import User, Post


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    description = FroalaEditor()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
