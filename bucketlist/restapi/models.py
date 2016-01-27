from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """Abstract model with bucketlist and items information"""
    name = models.CharField(blank=False, unique=True, max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Bucketlist(BaseModel):
    """A model of the bucketlist table"""
    created_by = models.ForeignKey(User)

    def __str__(self):
        return 'BucketList : {}'.format(self.name)


class BucketlistItem(BaseModel):
    """A model of the Bucketlist item table"""
    done = models.BooleanField(default=False)
    created_by = models.ForeignKey(User)
    bucketlist = models.ForeignKey(
        Bucketlist, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return 'Bucketlist Item : {}'.format(self.name)
