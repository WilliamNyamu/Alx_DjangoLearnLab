from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny]) # the permission classes should not be enclosed by single quotes.
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

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]