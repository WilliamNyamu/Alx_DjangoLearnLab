from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="signup"),
    path('login/', views.login_view, name='login'),
    path('profile/', views.ProfileListView.as_view(), name='profile'),

    path('auth/', include('rest_framework.urls'))
]