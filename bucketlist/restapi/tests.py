"""Test restapi app."""
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from faker import Faker
from .models import Bucketlist, BucketlistItem
import json
faker_instance = Faker()


class SetUpMixin(object):
    """Create the setup for TestCases."""

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        super(SetUpMixin, cls).setUpClass()
        cls.user_data = {
            'username': 'someone',
            'password': 'wordpass'
        }
        User.objects.create_user(**cls.user_data)
        cls.client = APIClient()


class UserAuthTestCase(SetUpMixin, APITestCase):
    """Test suite for user authentication."""

    def test_user_can_signup(self):
        """Test the user can signup for the service."""
        fake = Faker()
        username = fake.first_name()
        password = fake.name()
        data = {"username": username, "password": password}
        response = self.client.post('/auth/signup/', data=data)
        self.assertContains(response, username, status_code=201)

    def test_user_can_login(self):
        """Test that the user can be authenticated to access service."""
        response = self.client.post('/auth/', data=self.user_data)
        self.assertContains(response, 'token', status_code=200)


class BucketlistTestCase(SetUpMixin, APITestCase):
    """Test suite for the bucketlist model."""

    def test_user_can_create_bucketlist(self):
        """Test that the authenticated user can create a Bucketlist."""
        rv = self.client.post('/auth/', data=self.user_data)
        self.assertContains(rv, 'token', status_code=200)
        jwt_token = json.loads(rv.content)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(jwt_token.get('token')))
        bucketlist_data = {'name': 'After I get to D1...'}
        response = self.client.post(
            reverse('api.bucketlists'), bucketlist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_view_bucketlist(self):
        """Test that the authenticated user can create a Bucketlist."""
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
        res = self.client.get(
            reverse('api.bucketlist', kwargs={'pk': bucketlist.id}),
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_can_update_bucketlist(self):
        """Test that the authenticated user can update a Bucketlist."""
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
        """Ensure the use can delete an existing bucketlist."""
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


class BucketlistItemTestCase(SetUpMixin, APITestCase):
    """Test Suite for users action on a bucketlist item."""

    def test_user_can_create_bucketlist_item(self):
        """Ensure that user can make a bucketlist item."""
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
        pk = Bucketlist.objects.latest('date_created').pk
        bucketlist_item_data = {
            "bucketlist": pk, "name": "Make a drone", "done": False
        }
        res = self.client.post(
            reverse(
                'api.bucketlist.create', kwargs={'pk': pk}),
            bucketlist_item_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_can_update_bucketlist_item(self):
        """Ensure that user can update a bucketlist item."""
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
        pk = Bucketlist.objects.latest('date_created').pk
        bucketlist_item_data = {
            "bucketlist": pk, "name": "Make a drone", "done": False
        }
        res = self.client.post(
            reverse(
                'api.bucketlist.create', kwargs={'pk': pk}),
            bucketlist_item_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Edit the item done to be True
        update_item_data = {
            "bucketlist": pk, "name": "Make a drone", "done": True}
        item_id = BucketlistItem.objects.get(bucketlist=pk).pk
        res = self.client.put(
            reverse(
                'api.bucketlist.item', kwargs={'pk': pk, 'pk_item': item_id}),
            update_item_data,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_can_delete_bucketlist_item(self):
        """Ensure that user can delete a bucketlist item."""
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

        # Get the bucketlist pk
        pk = Bucketlist.objects.latest('date_created').pk
        bucketlist_item_data = {
            'bucketlist': pk, 'name': 'Make a good drone...', 'done': False}

        res = self.client.post(
            reverse('api.bucketlist.create', kwargs={'pk': pk}),
            bucketlist_item_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # get the newly created bucketlist item id
        item_id = BucketlistItem.objects.get(bucketlist=pk).pk
        res = self.client.delete(
            reverse(
                'api.bucketlist.item',
                kwargs={'pk': pk, 'pk_item': item_id}),
            format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class SearchBucketlistTestCase(SetUpMixin, APITestCase):
    """Test search functionality for bucketlist."""

    def test_user_can_search_bucketlist(self):
        """Ensure that the user can search for a given bucketlist.

        ENDPOINT: GET /bucketlists?q=:query.
        """
        rv = self.client.post('/auth/', data=self.user_data)
        self.assertContains(rv, 'token', status_code=200)
        jwt_token = json.loads(rv.content)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(jwt_token.get('token')))
        bucketlist_data = {'name': 'Before I get to D1'}
        another_one = {'name': 'Come back for more'}
        response = self.client.post(
            reverse('api.bucketlists'),
            bucketlist_data,
            format='json'
        )
        another_response = self.client.post(
            reverse('api.bucketlists'),
            another_one,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(another_response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(
            '{0}?q=Before I get'.format(reverse('api.bucketlists')),
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(
            response, 'Before I get to D1', status_code=200)

        response = self.client.get(
            '{0}?q=Bad search...'.format(reverse('api.bucketlists')),
            format='json')
        self.assertEqual(response.data, [])
