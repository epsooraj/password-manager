# Generated by Django 4.1 on 2022-08-11 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('password', '0006_password_strength'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to=settings.AUTH_USER_MODEL)),
                ('passwords', models.ManyToManyField(to='password.password')),
                ('users', models.ManyToManyField(to='password.access')),
            ],
            options={
                'db_table': 'organization',
            },
        ),
    ]
