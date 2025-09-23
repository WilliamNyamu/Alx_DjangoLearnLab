from django.http import request
from django.shortcuts import render
from .models import Author, Book, Library, Librarian
# Create your views here.

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.txt', {'books': books})