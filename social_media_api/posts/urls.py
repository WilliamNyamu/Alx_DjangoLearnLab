from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', views.PostView.as_view(), basename="posts")

urlpatterns = [
    path('', include(router.urls))
]