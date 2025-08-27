# tracker/tests/test_api.py
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

class ScoreTrackerAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="demo", email="d@d.com", password="password123")
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.auth = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}

    def test_create_semester(self):
        resp = self.client.post(
            "/api/semesters/",
            {"name": "2024/2025 - First", "level": "300L"},
            format="json",
            **self.auth
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["name"], "2024/2025 - First")

    def test_create_course_and_summary(self):
        # make semester
        s = self.client.post(
            "/api/semesters/", {"name": "2024/2025 - First", "level": "300L"},
            format="json", **self.auth
        ).data
        # add courses
        self.client.post("/api/courses/", {
            "semester": s["id"], "code": "MTH101", "title": "Calculus I", "unit": 3, "grade": "A"
        }, format="json", **self.auth)
        self.client.post("/api/courses/", {
            "semester": s["id"], "code": "PHY101", "title": "Physics", "unit": 2, "grade": "B"
        }, format="json", **self.auth)

        # summary
        sum_resp = self.client.get("/api/summary/", **self.auth)
        self.assertEqual(sum_resp.status_code, status.HTTP_200_OK)
        self.assertIn("cgpa", sum_resp.data)

from django.test import TestCase

class TrackerSanityTest(TestCase):
    def test_sanity(self):
        self.assertEqual(2 + 2, 4)
