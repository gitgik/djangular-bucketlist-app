from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import BucketlistSerializer, UserSerializer, \
    BucketlistItemsSerializer, ActionableBucketlistSerializer
from models import Bucketlist, BucketlistItem


class UserView(viewsets.ModelViewSet):
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
        return Bucketlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Saves the serialize POST data when creating a new bucketlist"""
        serializer.save(user_id=self.request.user.id)


class BucketlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Defines an actionable bucketlist view with Read, Update and Delete"""
    queryset = Bucketlist
    serializer_class = ActionableBucketlistSerializer
    permission_classes = (IsAuthenticated,)

    def get_query(self):
        """Specifies the object used for retrieve,
            update, and destrory actions"""
        return get_object_or_404(Bucketlist, pk=self.kwargs.get('pk'))


class BucketlistItemCreateView(generics.ListCreateAPIView):
    """Defines the bucketlist item creation behavior"""
    model = BucketlistItem
    serializer_class = BucketlistItemsSerializer

    def get_queryset(self):
        """Specifies the queryset used for the serialization"""
        pk = self.kwargs.get('pk')
        bucketlist = get_object_or_404(Bucketlist, pk=pk)
        return BucketlistItem.objects.filter(
            user=self.request.user, bucketlist=bucketlist)

    def perform_create(self, serializer):
        """Saves the serialize POST data to create a new bucketlist item"""
        pk = self.kwargs.get('pk')
        bucketlist = get_object_or_404(
            Bucketlist,
            pk=pk,
            user_id=self.request.user.id)
        serializer.save(bucketlist=bucketlist, user_id=self.request.user.id)


class BucketlistItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Defines an actionable bucketlist item view
       with Read, Update and Delete"""
    queryset = BucketlistItem
    serializer_class = BucketlistItemsSerializer

    def get_object(self):
        """Specifies the object used retrieve, update, destroy actions"""
        pk = self.kwargs.get('pk')
        # return an object of bucketlist items or raise a 404 if NotExists
        return get_object_or_404(BucketlistItem, pk=pk)
