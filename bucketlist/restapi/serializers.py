from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Defines the user api representation"""
    class Meta:
        model = User
        fields = ('username', 'email')

class BucketlistSerializer(serializers.ModelSerializer):
    """Defines the bucketlist api representation"""
    created_by = serializers.SerializerMethodField('get_creator')

    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'date_created', 'date_modified', 'created_by')

        def get_creator(self, obj):
            """Retrieves the creator of the bucketlist"""
            return obj.user.id

class ActionableBucketlistSerializer(serializers.ModelSerializer):
    """Defines an actionable bucketlist with child items"""
    items = serializers.SerializerMethodField('get_bucketlistitems')

    class Meta:
        models = Bucketlist
        fields = ('id', 'name', 'items', 'date_created', 'date_modified', 'created_by')

    def get_bucketlistitems(self, obj):
        """Returns a serializable list of bucketlist items"""
        queryset = list(BucketlistItems.objects.filter(bucketlist=obj))
        return [
            BucketlistItemSerializer(item).data for item in queryset
        ]

class BucketlistItemSerializer(serializers.ModelSerializer):
    """Defines the bucketlist api representation"""
    class Meta:
        model = BucketlistItems
        fields = ('id', 'name', 'done', 'date_created', 'date_modified')

class BucketlistItemCreateSerializer(serializers.ModelSerializer):
    """Defines the bucketlist item API representation for
       for the creation of a new bucketlist """

    class Meta:
        model = BucketlistItem



