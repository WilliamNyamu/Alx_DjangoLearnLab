from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="signup"),
    path('login/', views.login_view, name='login'),
    path('profile/', views.ProfileListView.as_view(), name='profile'),
    # Note that we use user_id because that is what is required as an argument by the follow_user function
    path('follow/<int:user_id>/', views.follow_user, name="follow-user"),
    path('unfollow/<int:user_id>/', views.unfollow_user, name="unfollow-user"),

    path('auth/', include('rest_framework.urls'))
]