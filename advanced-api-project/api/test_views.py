from django import test
from rest_framework.test import APITestCase
from .models import Book
from rest_framework import status

class ListTestCase(APITestCase):
    def setUp(self):
        self.url = "/api/books"
    
    def test_list_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)