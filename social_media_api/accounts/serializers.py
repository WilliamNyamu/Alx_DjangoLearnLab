from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture']

# Serializer handling user creation
class RegisterSerializer(serializers.ModelSerializer):
    # Password fields only writable - not readable in responses
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only = True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User # Remember we already declared that User is the get_user_model()
        fields = ['id', 'username', 'email', 'password', 'password2', 'token']

    def validate(self, attrs):
        """
        Ensure both passwords are the same
        Called automatically by DRF during serializer validation
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs # Always return the validated data
    
    def create(self, validated_data):
        """
        Create a new user instance with a securely hashed password
        Also generates an authentication token for the created user
        """
        # Remove the 'password2' because it's not part of the User model
        validated_data.pop('password2')
        # Using the get_user_model instead of the User to create the user
        user = get_user_model().objects.create_user(**validated_data)
        # Generate a token for the user
        Token.objects.create(user=user)
        # return the user object
        return user
    
    def get_token(self, obj):
        """
        Retrieve or create the token for a given user instance.
        This makes the token appear in the serialized response.
        """
        token, created = Token.objects.get_or_create(user=obj)
        return token.key
