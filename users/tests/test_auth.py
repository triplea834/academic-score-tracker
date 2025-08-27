# users/tests/test_auth.py
from rest_framework.test import APITestCase
from rest_framework import status

class AuthTests(APITestCase):
    def test_register_and_token(self):
        r = self.client.post("/api/auth/register/", {
            "username": "newbie", "email": "n@n.com", "password": "pass12345"
        }, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        t = self.client.post("/api/auth/token/", {
            "username": "newbie", "password": "pass12345"
        }, format="json")
        self.assertEqual(t.status_code, status.HTTP_200_OK)
        self.assertIn("token", t.data)

from django.test import TestCase

class TrackerSanityTest(TestCase):
    def test_sanity(self):
        self.assertEqual(2 + 2, 4)