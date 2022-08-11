from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse
from cryptography.fernet import Fernet

from . import models
from user import serializers as user_serializers


class SharedUserSerializer(serializers.ModelSerializer):
    user = user_serializers.UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source='user', queryset=User.objects.all())

    class Meta:
        model = models.Access
        fields = "__all__"


class PasswordSerializer(serializers.ModelSerializer):

    password_dc = serializers.SerializerMethodField()
    share_url = serializers.SerializerMethodField()
    complexity = serializers.SerializerMethodField()
    expired = serializers.SerializerMethodField()

    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Password
        fields = ('id', 'domain', 'password', 'password_dc', 'expiry', 'share_url',
                  'created_at', 'expired', 'complexity', 'user')
        read_only_fields = ('created_at', 'user')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        """Include default for read_only `user` field"""
        kwargs["user"] = self.fields["user"].get_default()

        # Encrypt password
        fernet = Fernet(settings.ENC_KEY)
        encPassword = fernet.encrypt(
            self.validated_data.pop('password').encode())
        kwargs["password"] = encPassword.decode()

        return super().save(**kwargs)

    def get_password_dc(self, obj):
        # Decrypt the obj.password
        fernet = Fernet(settings.ENC_KEY)
        return fernet.decrypt(bytes(obj.password, 'utf-8'))

    def get_share_url(self, obj):
        url = reverse('password-list',
                      args=[obj.id], request=self.context['request'])
        # Patch for . preceding the id in url
        url = url.replace('/.', '/')

        return url

    def get_complexity(self, obj):
        return "strong"

    def get_expired(self, obj):
        now = timezone.now()
        sub = now - obj.created_at
        return sub.days > obj.expiry
