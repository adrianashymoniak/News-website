from django.db import models
from froala_editor.fields import FroalaField

from news.models import User, Post


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None,
                               related_name="comments")
    description = FroalaField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.description)
