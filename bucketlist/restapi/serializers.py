from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Defines the user api model representation"""
    class Meta:
        model = User
        fields = ('username', 'email')

class BucketlistSerializer(serializers.ModelSerializer):
    """Defines the bucketlist api model representation"""
    created_by = serializers.SerializerMethodField('get_creator')

    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'date_created', 'date_modified', 'created_by')

        def get_creator(self, obj):
            """Retrieves the creator of the bucketlist"""
            return obj.user.id

