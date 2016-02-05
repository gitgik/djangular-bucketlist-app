from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Bucketlist, BucketlistItem


class UserSerializer(serializers.ModelSerializer):
    """Defines the user api representation"""
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        """Creates and returns a new user"""
        user = User.objects.create_user(**validated_data)
        return user


class BucketlistItemSerializer(serializers.ModelSerializer):
    """Defines the bucketlist item api representation"""
    class Meta:
        model = BucketlistItem
        fields = (
            'id', 'name', 'done',
            'date_created', 'date_modified', 'bucketlist')
        read_only_fields = ('date_modified', 'date_created')


class BucketlistSerializer(serializers.ModelSerializer):
    """Defines an actionable bucketlist api representation with child items"""

    items = BucketlistItemSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Bucketlist
        fields = (
            'id', 'name', 'items',
            'date_created', 'date_modified', 'created_by')
        read_only_fields = ('date_created', 'date_modified')
