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


    def test_refresh_token(self):
        login_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        refresh_token = login_response.cookies.get('refresh_token').value

        refresh_url = reverse('token_refresh')
        self.client.cookies['refresh_token'] = refresh_token
        refresh_response = self.client.post(refresh_url, {}, format='json')
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', refresh_response.cookies)
        self.assertIn('detail', refresh_response.data)
        self.assertEqual(refresh_response.data['detail'], "Token refreshed")

    def test_refresh_token_missing(self):
        refresh_url = reverse('token_refresh')
        refresh_response = self.client.post(refresh_url, {}, format='json')
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', refresh_response.data)
        self.assertEqual(refresh_response.data['detail'], "Refresh token not provided.")

    def test_refresh_token_invalid(self):
        refresh_url = reverse('token_refresh')
        self.client.cookies['refresh_token'] = 'invalidtoken'
        refresh_response = self.client.post(refresh_url, {}, format='json')
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', refresh_response.data)
        self.assertEqual(refresh_response.data['detail'], "Invalid refresh token.")