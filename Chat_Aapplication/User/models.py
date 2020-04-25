from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out

class UsersData(models.Model):
    username = models.CharField(blank=False, max_length=100)
    email = models.EmailField(blank=True)
    password1 = models.CharField(max_length=60)
    password2 = models.CharField(max_length=60)

    def __str__(self):
        return self.username

class LoggedUser(models.Model):
    username = models.CharField(max_length=30, primary_key=True)

    def __unicode__(self):
        return self.username


def login_user(sender, request, user, **kwargs):
    LoggedUser(username=user.username).save()


def logout_user(sender, request, user, **kwargs):
    try:
        u = LoggedUser.objects.get(pk=user.username)
        u.delete()
    except LoggedUser.DoesNotExist:
        pass


user_logged_in.connect(login_user)
user_logged_out.connect(logout_user)