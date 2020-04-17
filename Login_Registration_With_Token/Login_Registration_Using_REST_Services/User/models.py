from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
class UsersData(models.Model):
    username = models.CharField(blank=False, max_length=100)
    email = models.EmailField(blank=True)
    password1 = models.CharField(max_length=60)
    password2 = models.CharField(max_length=60)

    def __str__(self):
        return self.username

       
class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}
