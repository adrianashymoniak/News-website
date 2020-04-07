import logging

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand

ALL_GROUPS = ['admins', 'moderators', 'users']
MODELS = ['post']
ALL_PERMISSIONS = ['view', 'change', 'add', 'delete']
MODERATORS_PERMISSIONS = ['view', 'change']


class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'

    def handle(self, *args, **options):
        for group in ALL_GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                if ('admins' in group) or ('users' in group):
                    Command.permission_setter(ALL_PERMISSIONS, model,
                                              new_group)
                else:
                    Command.permission_setter(MODERATORS_PERMISSIONS, model,
                                              new_group)

        print("Created default group and permissions.")

    @staticmethod
    def permission_setter(items, model, new_group):
        for item in items:
            name = 'Can {} {}'.format(item, model)
            print('Creating {}'.format(name))

            try:
                model_add_perm = Permission.objects.get(name=name)
            except Permission.DoesNotExist:
                logging.warning(
                    "Permission not found with name '{}'.".format(
                        name))
                continue

            new_group.permissions.add(model_add_perm)
