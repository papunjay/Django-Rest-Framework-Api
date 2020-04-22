from rest_framework import serializers
from ChatApp.models import Message
class Message_serializers(serializers.ModelSerializer):


    class meta:
        model=Message
        fields=['indentifier_message_number','messages','rating','From']