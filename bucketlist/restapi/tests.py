from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from faker import Faker
from .models import Bucketlist, BucketlistItem
import json


faker_instance = Faker()


class SetUpMixin(object):
    """Create the setup for TestCases"""
    @classmethod
    def setUpClass(cls):
        super(SetUpMixin, cls).setUpClass()
        cls.user_data = {
            'username': 'someone',
            'password': 'wordpass'
        }
        User.objects.create_user(**cls.user_data)
        cls.client = APIClient()


class UserAuthTestCase(SetUpMixin, APITestCase):
    def test_user_can_login(self):
        """Test that the user can be authenticated to access service"""
        response = self.client.post('/auth/', data=self.user_data)
        self.assertContains(response, 'token', status_code=200)
