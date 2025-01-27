from django.db import IntegrityError
from rest_framework import serializers
from .models import Followers


class FollowersSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        models = Followers
        fields = [
            'id', 'owner', 'followed', 'created_at', 'followed_name'
        ]

    def create(self, validated_data):
        '''
        Handles duplication errors
        '''
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })