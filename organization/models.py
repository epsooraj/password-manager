from django.db import models
from django.contrib.auth.models import User

from password import models as password_models


class OrganizationPassword(models.Model):
    password = models.ForeignKey(
        to=password_models.Password, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.password)


class Organization(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='organizations')

    shared_users = models.ManyToManyField(to=password_models.Access)

    passwords = models.ManyToManyField(to=OrganizationPassword)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        db_table = 'organization'
