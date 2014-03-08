import sys

from django import get_version
from django.core.management.base import BaseCommand, CommandError

from django_ftpserver import models


class Command(BaseCommand):
    help = "Create FTP user account"
    args = "username group [home_dir]"

    def get_user_model(self):
        if get_version() >= '1.5':
            from django.contrib.auth import get_user_model
            return get_user_model()
        from django.contrib.auth.models import User
        return User

    def handle(self, *args, **options):
        if len(args) < 2:
            raise CommandError("Enter the username and group name.")
        username = args[0]
        group_name = args[1]
        if len(args) > 2:
            home_dir = args[2]
        else:
            home_dir = None

        if models.FTPUserAccount.objects.filter(
                user__username=username).exists():
            raise CommandError(
                'FTP user account "{username}" is already exists.'.format(
                    username=username))

        user_model = self.get_user_model()
        try:
            user = user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            raise CommandError(
                'User "{username}" is not exists.'.fomat(username=username))

        try:
            group = models.FTPUserGroup.objects.get(name=group_name)
        except models.FTPUserGroup.DoesNotExist:
            raise CommandError(
                'FTP user group "{name}" is not exists.'.fomat(
                    name=group_name))

        account = models.FTPUserAccount.create(
            user=user, group=group, home_dir=home_dir)

        sys.stdout.write(
            'FTP user account pk={pk}, "{username}" was created.\n'.format(
                pk=account.pk, username=username))
