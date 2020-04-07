from django.db import models


class CustomGroup(models.Model):
    group = models.OneToOneField('auth.Group', unique=True,
                                 on_delete=models.CASCADE)

    pre_moderation = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(self.group.name)
