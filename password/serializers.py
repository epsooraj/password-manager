from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse
from cryptography.fernet import Fernet
from password_strength import PasswordStats

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
    expired = serializers.SerializerMethodField()

    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Password
        fields = ('id', 'domain', 'password', 'password_dc', 'expiry', 'share_url',
                  'created_at', 'expired', 'strength', 'user')
        read_only_fields = ('created_at', 'user', 'strength')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        # Include default for read_only `user` field
        kwargs["user"] = self.fields["user"].get_default()

        # Encrypt password
        passwd = self.validated_data.pop('password')
        fernet = Fernet(settings.ENC_KEY)
        encPassword = fernet.encrypt(passwd.encode())
        kwargs["password"] = encPassword.decode()

        # Password strength
        stats = PasswordStats(passwd)
        print(stats.strength())
        kwargs['strength'] = stats.strength() * 100

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

    def get_expired(self, obj):
        now = timezone.now()
        sub = now - obj.created_at
        return sub.days > obj.expiry
