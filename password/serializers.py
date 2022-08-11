from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse

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

    password = serializers.SerializerMethodField()
    share_url = serializers.SerializerMethodField()
    complexity = serializers.SerializerMethodField()
    expired = serializers.SerializerMethodField()

    class Meta:
        model = models.Password
        fields = ('id', 'domain', 'passwd', 'password', 'expiry', 'share_url',
                  'created_at', 'expired', 'complexity', 'user')
        read_only_fields = ('created_at', 'user')

    def save(self, **kwargs):
        """Include default for read_only `user` field"""
        kwargs["user"] = self.fields["user"].get_default()
        return super().save(**kwargs)

    def get_password(self, obj):
        # Decrypt the obj.passwd
        return obj.passwd

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
