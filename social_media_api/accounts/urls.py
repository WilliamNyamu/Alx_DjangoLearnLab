from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/signup/', views.RegisterView.as_view(), name="signup"),
    path('auth/login/', views.login_view, name='login'),
    path('profile/', views.ProfileListView.as_view(), name='profile'),

    path('auth/', include('rest_framework.urls'))
]