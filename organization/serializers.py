from rest_framework import serializers

from . import models
from password import models as password_models
from password import serializers as password_serializers


class OrganizationPasswordSerializer(serializers.ModelSerializer):

    password = password_serializers.PasswordSerializer(read_only=True)
    password_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source='password', queryset=password_models.Password.objects.all())

    class Meta:
        model = models.OrganizationPassword
        fields = "__all__"


class OrganizationSerializer(serializers.ModelSerializer):

    shared_users = password_serializers.SharedUserSerializer(
        many=True, read_only=True)
    passwords = OrganizationPasswordSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Organization
        fields = ('id', 'name', 'passwords', 'user',
                  'shared_users', 'created_at')
        read_only_fields = ('user', 'created_at')

    def save(self, **kwargs):
        # Include default for read_only `user` field
        kwargs["user"] = self.fields["user"].get_default()
        return super().save(**kwargs)
