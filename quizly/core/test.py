"""
Tests for the health check endpoint.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthTests(APITestCase):
    """
    Ensure that the /health/ endpoint responds correctly.
    """

    def test_health_ok(self):
        """
        The health endpoint should return status 200 and {"status": "ok"}.
        """
        url = reverse("health")
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"status": "ok"})
