from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthTests(APITestCase):

    def test_health_ok(self):
        url = reverse("health")
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"status": "ok"})
