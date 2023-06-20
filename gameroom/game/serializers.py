from . import models
from rest_framework import serializers


class PlayerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = models.Player
        fields = ['id', 'user', 'user_id', 'score']

