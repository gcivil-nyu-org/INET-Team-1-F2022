from django.test import TestCase
from django.urls import reverse

class TestViews(TestCase):
    def test_main_index(self):
        url_path = ''
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)