from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
User=get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User,related_name='author_message',on_delete=models.CASCADE)
    #author = models.ForeignKey(User)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_message(self):
        return Message.objects.order_by('-timestamp').all()[:10]



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