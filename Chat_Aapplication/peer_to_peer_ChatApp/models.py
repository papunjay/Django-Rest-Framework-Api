from django.db import models
from django.contrib.auth import get_user_model
#from django.contrib.auth.signals import user_logged_in, user_logged_out
User=get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User,related_name='author_message',on_delete=models.CASCADE)
    #author = models.ForeignKey(User)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_message(self):
        return Message.objects.order_by('-timestamp').all()[:]




