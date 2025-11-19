"""
Health check endpoint.

Used to verify that the API is reachable and operational.
"""

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class HealthView(APIView):
    """
    Public health check endpoint.

    Returns:
        {"status": "ok"} with HTTP 200 to indicate the API is running.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        """
        Handle GET requests to the health endpoint.
        """
        return Response({"status": "ok"})
