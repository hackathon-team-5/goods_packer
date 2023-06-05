from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'first_name': 'testuser_first_name',
            'last_name': 'testuser_last_name',
            'password': 'testpassword'
        }

    def test_create_user(self):
        """
        New user creation test.
        """
        response = self.client.post('/api/users/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(username=self.user_data['username']).exists()
        )

    def test_create_user_invalid_data(self):
        """
        Check that creating a user with invalid data fails.
        """
        invalid_user_data = [
            {
                'username': 'testuser',
                'password': 'testpassword'
            },
            {
                'username': 'te',
                'first_name': 'testuser_first_name',
                'last_name': 'testuser_last_name',
                'password': 'testpassword'
            },
        ]
        for data in invalid_user_data:
            response = self.client.post('/api/users/', data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertFalse(
                User.objects.filter(
                    username=data['username']).exists()
            )
            if data == invalid_user_data[0]:
                self.assertTrue(
                    'This field is required.' in response.data['first_name']
                )

    def test_get_token(self):
        """
        Checking token receipt.
        """
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)
        response = self.client.post('/api/auth/token/login/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('auth_token' in response.data)

    def test_not_auth_logout(self):
        """
        Logout test and cancellation of token by unauthorized user.
        """
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)
        response = self.client.post('/api/auth/token/logout/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        """
        Logout test and token cancellation.
        """
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)
        response = self.client.post(
            '/api/auth/token/logout/', HTTP_AUTHORIZATION=(
                f'Token {self.token.key}')
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(user=self.user).exists())
