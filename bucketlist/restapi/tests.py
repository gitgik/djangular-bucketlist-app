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


class BucketlistTestCase(SetUpMixin, APITestCase):
    def test_user_can_create_bucketlist(self):
        """Tests that the authenticated user can create a Bucketlist"""
        rv = self.client.post('/auth/', data=self.user_data)
        self.assertContains(rv, 'token', status_code=200)
        jwt_token = json.loads(rv.content)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(jwt_token.get('token')))
        bucketlist_data = {'name': 'After I get to D1...'}
        response = self.client.post(
            reverse('api.bucketlists'), bucketlist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_update_bucketlist(self):
        """Tests that the authenticated user can create a Bucketlist"""
        rv = self.client.post('/auth/', data=self.user_data)
        self.assertContains(rv, 'token', status_code=200)
        jwt_token = json.loads(rv.content)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(jwt_token.get('token')))
        bucketlist_data = {'name': 'After I get to D1...'}
        response = self.client.post(
            reverse('api.bucketlists'), bucketlist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        bucketlist = Bucketlist.objects.get()
        bucketlist_data = {'name': 'before i die...'}
        res = self.client.put(
            reverse('api.bucketlist', kwargs={'pk': bucketlist.id}),
            bucketlist_data, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_can_delete_bucketlist(self):
        """Ensures the use can delete an existing bucketlist"""
        rv = self.client.post('/auth/', data=self.user_data)
        self.assertContains(rv, 'token', status_code=200)
        jwt_token = json.loads(rv.content)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(jwt_token.get('token')))
        bucketlist_data = {'name': 'Before I get to D1'}
        response = self.client.post(
            reverse('api.bucketlists'),
            bucketlist_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        bucketlist = Bucketlist.objects.get()
        response = self.client.delete(
            reverse('api.bucketlist', kwargs={'pk': bucketlist.id}),
            {},
            format='json',
            follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)















