from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class LogoutTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "confirmed_password": "testpassword",
        }
        self.client.post(reverse('register'), self.user_data, format='json')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_logout_user(self):
        login_data = {"username": "testuser", "password": "testpassword"}
        login_response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        access = login_response.cookies.get('access_token').value
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        self.client.cookies['refresh_token'] = login_response.cookies.get('refresh_token').value

        logout_response = self.client.post(self.logout_url, {}, format='json')
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            logout_response.data['detail'],
            "Log-Out successfully! All tokens deleted. Refresh token is now invalid."
        )

    def test_logout_with_invalid_refresh_token_triggers_tokenerror(self):
        login_data = {"username": "testuser", "password": "testpassword"}
        login_response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        access = login_response.cookies.get('access_token').value
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

        self.client.cookies['refresh_token'] = "invalid.refresh.token"

        logout_response = self.client.post(self.logout_url, {}, format='json')

        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            logout_response.data['detail'],
            "Log-Out successfully! All tokens deleted. Refresh token is now invalid."
        )