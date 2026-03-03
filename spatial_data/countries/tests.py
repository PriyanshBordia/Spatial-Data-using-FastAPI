from django.test import TestCase, Client
from django.urls import reverse


class UrlTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_upload_page_loads(self):
        response = self.client.get(reverse("upload"))
        self.assertEqual(response.status_code, 200)

    def test_add_country_page_loads(self):
        response = self.client.get(reverse("add_country"))
        self.assertEqual(response.status_code, 200)
