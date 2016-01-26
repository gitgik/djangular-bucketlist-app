from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """Abstract model with bucketlist and items information"""
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    """A model representation of the user"""
    bio = models.TextField(blank=True, null=True)
    age = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User)


class Bucketlist(BaseModel):
    """A model of the bucketlist table"""
    user = models.ForeignKey(User)

    def num_items_done(self):
        """Returns number of bucketlist items completed"""
        return self.bucketlist_set.filter(done=True).count()


class BucketlistItem(BaseModel):
    """A model of the Bucketlist item table"""
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    bucketlist = models.ForeignKey(Bucketlist)
