from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'first_name': 'testuser_first_name',
            'last_name': 'testuser_last_name',
            'password': 'testpassword'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)

    def test_get_users(self):
        """
        The test for getting a list of users.
        """
        response = self.client.get(
            '/api/users/',
            HTTP_AUTHORIZATION=(f'Token {self.token.key}')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0].get('username'),
            self.user_data['username']
        )

    def test_get_user_profile(self):
        """
        The test for obtaining a user profile.
        """
        response = self.client.get(
            f'/api/users/{self.user.id}/',
            HTTP_AUTHORIZATION=(f'Token {self.token.key}')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_not_get_user_profile(self):
        """
        The test of not getting a user profile.
        """
        response = self.client.get(
            f'/api/users/{self.user.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_current_user(self):
        """
        The test for getting the current user.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_not_set_password(self):
        """
        Checking for incorrect user password changes.
        """
        self.client.force_authenticate(user=self.user)
        new_password_data = [
            {
                'new_password': 'testpassword',
                'current_password': 'testpassword'
            },
            {
                'new_password': 'newtestpassword1',
            },
        ]
        for password in new_password_data:
            response = self.client.post(
                '/api/users/set_password/', password
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            if password == new_password_data[1]:
                self.assertTrue(
                    ('This field is required.'
                        in response.data['current_password'])
                )

    def test_set_password(self):
        """
        Checking user password changes.
        """
        self.client.force_authenticate(user=self.user)
        new_password_data = {
            'new_password': 'newtestpassword1',
            'current_password': 'testpassword'
        }
        response = self.client.post(
            '/api/users/set_password/', new_password_data
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            self.user.check_password(new_password_data['current_password'])
        )
        self.assertTrue(
            self.user.check_password(new_password_data['new_password'])
        )

    def test_not_auth_set_password(self):
        """
        Checking for password changes by an unauthorized user.
        """
        new_password_data = {
            'new_password': 'newtestpassword1',
            'current_password': 'testpassword'
        }
        response = self.client.post(
            '/api/users/set_password/', new_password_data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
