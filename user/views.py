from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny

from . import serializers


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegisterSerializer
