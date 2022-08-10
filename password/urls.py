from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register('', viewset=views.PasswordViewSet, basename='password')

urlpatterns = [
    path('', include(router.urls), name='password-url')
]
