from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class LoginTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "confirmed_password": "testpassword"
        }
        self.client.post(reverse('register'), self.user_data, format='json')
        self.login_url = reverse('login')

    def test_login_user(self):
        login_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], "Login successfully!")
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], "testuser")

    def test_login_invalid_credentials(self):
        login_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)