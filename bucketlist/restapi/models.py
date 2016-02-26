from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
import re


def normalize(query_string):
    """Return a tuple of words from a query statement"""
    terms = re.compile(r'"([^"]+)"|(\S+)').findall(query_string)
    normspace = re.compile(r'\s{2,}').sub
    return (normspace(' ', (t[0] or t[1]).strip()) for t in terms)


class BaseModel(models.Model):
    """Abstract model with bucketlist and items information"""
    name = models.CharField(blank=False, unique=True, max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    @classmethod
    def search(cls, query_string):
        """Searches the model table for words similar to the query string"""
        query_terms = normalize(query_string)
        for word in query_terms:
            query_object = models.Q(**{"name__icontains": word})
            return cls.objects.filter(query_object).order_by('date_created')


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
