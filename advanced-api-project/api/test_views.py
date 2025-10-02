from django import test
from rest_framework.test import APITestCase
from .models import Book, Author
from rest_framework import status
from django.contrib.auth.models import User

class ListTestCase(APITestCase):
    def setUp(self):
        self.url = "/api/books/"
    
    def test_list_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class CreateTestCase(APITestCase):
    def setUp(self):
        self.url = "/api/books/create"
        self.author = Author.objects.create(name="George Orwell")
        self.user = User.objects.create_user(username="waridi", password="12345")
    
    def test_create_book(self):
        # setting up authentication
        logged_in = self.client.login(username="waridi", password="12345")
        self.assertTrue(logged_in)
        
        data = {
            'title': '1984',
            'publication_year': 1949,
            'author': self.author.id
        }
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data[0]['title'], '1984')