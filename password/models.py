from django.db import models
from django.contrib.auth.models import User


class Access(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='access_users', verbose_name='User')

    PERMISSION_CHOICES = (
        ('r', 'Read'),
        ('w', 'Write')
    )
    permission = models.CharField(max_length=1, choices=PERMISSION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{str(self.user)} - {str(self.permission)}'

    class Meta:
        db_table = 'access'


class Password(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='passwords', verbose_name='User')
    created_at = models.DateTimeField(auto_now_add=True)

    domain = models.CharField(max_length=100, verbose_name='Domain')
    password = models.TextField(verbose_name='Password')
    expiry = models.IntegerField(verbose_name='Expiry in days', default=-1)
    strength = models.IntegerField(verbose_name='Strength', default=0)

    access_users = models.ManyToManyField(to=Access)

    def __str__(self) -> str:
        return f'{str(self.user)} - {str(self.domain)}'

    class Meta:
        db_table = 'password'
