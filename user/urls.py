from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as rauth_views

from . import views as user_views

urlpatterns = [
    path('login/', rauth_views.obtain_auth_token, name='login'),
    path('register/', user_views.RegisterView.as_view(), name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
