from django.test import SimpleTestCase, RequestFactory
from rest_framework import exceptions
from unittest.mock import patch

from auth_app.api.authentication import CookieJWTAuthentication


class CookieJWTAuthenticationTests(SimpleTestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_invalid_cookie_raises_authentication_failed(self):
        request = self.rf.get("/")
        request.COOKIES["access_token"] = "invalidtoken"

        auth = CookieJWTAuthentication()

        # Force `get_validated_token` to raise so the except-branch is exercised
        with patch.object(CookieJWTAuthentication, "get_validated_token", side_effect=Exception("boom")):
            with self.assertRaises(exceptions.AuthenticationFailed):
                auth.authenticate(request)
