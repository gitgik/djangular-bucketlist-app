from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import BucketlistSerializer, UserSerializer, \
    BucketlistItemSerializer
from models import Bucketlist, BucketlistItem


class UserView(generics.CreateAPIView):
    """Defines the user view"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BucketlistView(generics.ListCreateAPIView):
    """Defines the Bucketlist list view behavior"""
    serializer_class = BucketlistSerializer
    permission_classes = (IsAuthenticated,)
    paginate_by = 100

    def get_queryset(self):
        """Specifies the queryset used for serialization"""
        q = self.request.GET.get('q', None)
        if q:
            return Bucketlist.search(q)
        return Bucketlist.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """Saves the serialize POST data when creating a new bucketlist"""
        serializer.save(created_by=self.request.user)


class BucketlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Defines an actionable bucketlist view with Read, Update and Delete"""
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (IsAuthenticated,)


class BucketlistItemCreateView(generics.ListCreateAPIView):
    """Defines the bucketlist item creation behavior"""
    queryset = BucketlistItem
    serializer_class = BucketlistItemSerializer

    def get_queryset(self):
        """Specifies the queryset used for the serialization"""
        pk = self.kwargs.get('pk')
        bucketlist = get_object_or_404(Bucketlist, pk=pk)
        return BucketlistItem.objects.filter(
            created_by=self.request.user, bucketlist=bucketlist)

    def perform_create(self, serializer):
        """Saves the serialize POST data to create a new bucketlist item"""
        pk = self.kwargs.get('pk')
        bucketlist = get_object_or_404(
            Bucketlist,
            pk=pk,
            created_by=self.request.user)
        serializer.save(bucketlist=bucketlist, created_by=self.request.user)


class BucketlistItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Defines an actionable bucketlist item view
       with Read, Update and Delete"""
    queryset = BucketlistItem.objects.all()
    serializer_class = BucketlistItemSerializer

    def get_object(self):
        """Specifies the object used for `update`,
         `retrieve`, `destroy` actions"""
        pk_item = self.kwargs.get('pk_item')
        return get_object_or_404(BucketlistItem, pk=pk_item)
