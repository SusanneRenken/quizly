from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class RegistrationTests(APITestCase):

    def test_create_user(self):
        url = reverse('register')
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "confirmed_password": "testpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_create_user_password_mismatch(self):
        url = reverse('register')
        data = {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "testpassword",
            "confirmed_password": "mismatchedpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="testuser2").exists())