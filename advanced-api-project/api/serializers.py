from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate(self, data):
        from datetime import datetime
        current_date = datetime.now()
        current_year = current_date.year
        if data['publication_year'] > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future")
        return data



class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['name', 'books']

