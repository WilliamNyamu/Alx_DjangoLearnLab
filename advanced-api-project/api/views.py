from django.shortcuts import render
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
# Create your views here.

class ListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class DetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class CreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



