from django.db import models

from news.models import User


class Post(models.Model):
    DECLINED = -1
    IN_MODERATION = 0
    ACCEPTED = 1

    Status = (
        (DECLINED, 'Declined'),
        (IN_MODERATION, 'In moderation'),
        (ACCEPTED, 'Accepted'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    status = models.IntegerField(choices=Status, default=IN_MODERATION)

    def __str__(self):
        return self.title
