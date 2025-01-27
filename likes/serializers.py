from rest_framework import serializers
from .models import Likes


class LikesSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Likes
        fields = [
            'id', 'owner', 'post', 'created_at'
        ]