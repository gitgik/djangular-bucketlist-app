from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Bucketlist, BucketlistItem


class UserSerializer(serializers.ModelSerializer):
    """Defines the user api representation"""
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        """Creates and returns a new user"""
        user = User(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class BucketlistItemSerializer(serializers.ModelSerializer):
    """Defines the bucketlist api representation"""
    class Meta:
        model = BucketlistItem
        fields = ('id', 'name', 'done', 'date_created', 'date_modified')
        read_only_fields = ('items', 'date_created', 'date_modified')


class BucketlistSerializer(serializers.ModelSerializer):
    """Defines an actionable bucketlist with child items"""

    items = BucketlistItemSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Bucketlist
        fields = (
            'id', 'name', 'items',
            'date_created', 'date_modified', 'created_by'
        )


class ActionableBucketlistSerializer(serializers.ModelSerializer):
    """Defines an actionable bucketlist with child items"""
    items = serializers.SerializerMethodField('get_bucketlistitems')

    class Meta:
        models = Bucketlist
        fields = (
            'id', 'name', 'items',
            'date_created', 'date_modified', 'created_by')

    def get_bucketlistitems(self, obj):
        """Returns a serializable list of bucketlist items"""
        queryset = list(BucketlistItem.objects.filter(bucketlist=obj))
        return [
            BucketlistItemSerializer(item).data for item in queryset
        ]


class BucketlistItemCreateSerializer(serializers.ModelSerializer):
    """Defines the bucketlist item API representation for
       for the creation of a new bucketlist """

    class Meta:
        model = BucketlistItem
