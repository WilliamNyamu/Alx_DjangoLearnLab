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
from rest_framework.authentication import get_user_model
from rest_framework import generics
from rest_framework import permissions
from rest_framework import views

User = get_user_model()

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow a user.
    Concept to understand is the reverse relationship and how they work.
    """
    try:
        user_to_follow = User.objects.get(id = user_id) # Get the user_to_follow instance
    except User.DoesNotExist:
        return Response(
            {'error':'User not found'},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Use the request.user for the authenticated user. You might find youself using User model which is WRONG
    if user_to_follow in request.user.following.all():
        return Response(
            {'detail': f'You already follow {user_to_follow.username}'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Prevent users from following themselves
    if user_to_follow == request.user:
        return Response(
            {'error': 'You cannot follow yourself'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    request.user.following.add(user_to_follow)
    return Response(
        {'message': f'You are now following {user_to_follow.username}'},
        status = status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        user_to_unfollow = User.objects.get(id=user_id) # Get the specific user instance to unfollow
    except User.DoesNotExist:
        return Response(
            {'error':'User not found'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check whether the user_to_unfollow exists in the list of following users
    if not request.user.following.filter(id = user_to_unfollow.id).exists():
        return Response(
            {
                'error': f'You do not follow {user_to_unfollow.username}'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    request.user.following.remove(user_to_unfollow)
    return Response(
        {
            'message': f'You have successfully unfollowed {user_to_unfollow.username}'
        },
        status=status.HTTP_200_OK
    )

# A simpler, class-based view on following and unfollowing using APIView and overriding the post method
class FollowToggleView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, user_id):
        me = request.user
        try:
            other = CustomUser.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'detail':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if other == me:
            return Response({'detail':'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        if other in me.following.all():
            me.following.remove(other)
            action = 'unfollowed'
        else:
            me.following.add(other)
            # Notification.objects.create(recipient=other, actor=me, verb='followed you')
            action = 'followed'
        return Response({'status': action})