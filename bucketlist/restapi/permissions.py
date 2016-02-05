from rest_framework.permissions import BasePermission
from .models import BucketlistItem


class IsOwnerOrReadOnly(BasePermission):
    """Setting permission class to isOwner or read only"""
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, BucketlistItem):
            return obj.bucketlist.created_by == request.user
        return obj.created_by == request.user
