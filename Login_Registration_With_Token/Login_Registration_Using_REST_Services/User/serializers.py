from rest_framework import serializers
from .models import UsersData
from django.contrib.auth.models import User

class RegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = UsersData
        fields = '__all__'
        extra_kwargs = {
            'password1': {
                'write_only': True
            },
            'password2': {
                'write_only': True
            }
        }

class ResetSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'password'