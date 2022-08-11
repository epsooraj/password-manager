from django.urls import path, include
from rest_framework import routers

from . import views

password_router = routers.DefaultRouter()
password_router.register(
    '', viewset=views.PasswordViewSet, basename='password')

share_router = routers.DefaultRouter()
share_router.register('',
                      viewset=views.SharePermissionViewSet, basename='shared-user')

urlpatterns = [
    path('', include(password_router.urls)),
    path('<int:pid>/share/', include(share_router.urls)),
]
