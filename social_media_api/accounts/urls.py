from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="signup"),
    path('login/', views.login_view, name='login'),
    path('profile/', views.ProfileListView.as_view(), name='profile'),
    # Note that we use user_id because that is what is required as an argument by the follow_user function
    path('<int:user_id>/follow/', views.follow_user, name="follow-user"),
    path('<int:user_id>/unfollow/', views.unfollow_user, name="unfollow-user"),

    path('auth/', include('rest_framework.urls'))
]