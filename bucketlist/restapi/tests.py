from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from faker import Faker
from .models import Bucketlist
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

    def test_user_can_view_bucketlist(self):
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
        res = self.client.get(
            reverse('api.bucketlist', kwargs={'pk': bucketlist.id}),
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_can_update_bucketlist(self):
        """Tests that the authenticated user can update a Bucketlist"""
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


class BucketlistItemTestCase(SetUpMixin, APITestCase):
    """Test Suite for users action on a bucketlist item"""

    def test_user_can_create_bucketlist_item(self):
        """Ensures that user can make a bucketlist item"""
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
        bucketlist_item_data = {"name": "Make a drone", "done": False}
        res = self.client.post(
            reverse('api.bucketlist.create', kwargs={'pk': pk}),
            bucketlist_item_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_can_update_bucketlist_item(self):
        """Ensures that user can make a bucketlist item"""
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

        bucketlist_item_data = {'name': 'Make a drone', 'done': False}
        res = self.client.post(
            reverse('api.bucketlist.create', kwargs={'pk': 1}),
            bucketlist_item_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Edit the item done to be True
        item = {'name': 'Make a drone', 'done': True}
        res = self.client.put(
            reverse('api.bucketlist.item', kwargs={'pk': 1, 'id': 1}),
            item,
            format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # test for data that has been updated
        res = self.client.get(
            reverse('api.bucketlist.item',
                    kwargs={'pk': 1, 'id': 1}), format='json')
        rv_item = json.loads(res.content)
        self.assertEqual(rv_item['done'], item['done'])

    def test_user_can_delete_bucketlist_item(self):
        """Ensures that user can make a bucketlist item"""
        rv = self.client.post('/auth/', data=self.user_data)
        self.assertContains(rv, 'token', status_code=200)
        jwt_token = json.loads(rv.content)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(jwt_token.get('token')))
        bucketlist_data = {'name': 'Before I get to D1'}
        bucketlist_data1 = {'name': 'Another one!'}

        response = self.client.post(
            reverse('api.bucketlists'),
            bucketlist_data,
            format='json'
        )
        # create another one(bucketlist)
        response = self.client.post(
            reverse('api.bucketlists'),
            bucketlist_data1,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        bucketlist_item_data = {
            'id': 1, 'name': 'Make a drone...', 'done': False}

        res = self.client.post(
            reverse('api.bucketlist.create', kwargs={'pk': 1}),
            bucketlist_item_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.delete(
            reverse('api.bucketlist.item', kwargs={'pk': 1, 'id': 1}),
            format='json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class SearchBucketlistTestCase(SetUpMixin, APITestCase):
    """Test search functionality for bucketlist"""

    def test_user_can_search_bucketlist(self):
        """Ensures that the user can search for a given bucketlist
        ENDPOINT: GET /bucketlists?q=:query
        """
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

        response = self.client.get(
            '{0}?q=Before I get'.format(reverse('api.bucketlists')),
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
