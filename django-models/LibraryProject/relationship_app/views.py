from.models import Library
from django.http import request
from django.shortcuts import render
from .models import Author, Book, Librarian
from django.views.generic import ListView, DetailView
# Create your views here.

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'