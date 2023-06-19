from . import models
from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Player
        fields = ['user', 'score']