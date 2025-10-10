from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView, RetrieveAPIView

# Create your views here.
@api_view(['POST'])
@permission_classes(['AllowAny'])
def register_view(request):
    """ Function to register new users """
    username = request.data.get['username']
    password = request.data.get['password']
    email = request.data.get['email']

    # Validation Checks
    # Check whether the user has entered the username and password
    if not username or not password:
        return Response(
            {'error': 'Please enter a username and a password!'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Check whether the username exists
    if CustomUser.objects.filter(username=username).exists():
        return Response(
            {'error': 'username entered already exists. Pick another one!'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check whether the email already exists
    if CustomUser.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already exists! It should be unique'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create the user and store them in the variable 'user'
    user = CustomUser.objects.create_user(username=username, password=password, email=email)
    
    # Generate a token for them. We are using TokenAuthentication
    token = Token.objects.create(user=user)

    # Return the response below
    return Response(
        {
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'message': 'User created successfully'
        },
        status=status.HTTP_201_CREATED
    )
    
@api_view(['POST'])
@permission_classes(['AllowAny'])
def login_view(request):
    username= request.data.get('username')
    password = request.data.get('password')

    # Check whether the username and password have been entered
    if not username or not password:
        return Response(
            {'error': 'username and password have to be entered'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response (
            {
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'message': "User login successful"
            },
            status= status.HTTP_200_OK
        )
    else:
        return Response (
            {
                'error': "Login failed! Try later"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class ProfileListView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = IsAuthenticated