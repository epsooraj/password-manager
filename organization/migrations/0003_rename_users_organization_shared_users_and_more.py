# Generated by Django 4.1 on 2022-08-11 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_organization_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='users',
            new_name='shared_users',
        ),
        migrations.RenameField(
            model_name='organization',
            old_name='owner',
            new_name='user',
        ),
    ]
