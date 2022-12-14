# Generated by Django 4.1 on 2022-08-11 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('password', '0006_password_strength'),
        ('organization', '0003_rename_users_organization_shared_users_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('password', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='password.password')),
            ],
        ),
        migrations.AlterField(
            model_name='organization',
            name='passwords',
            field=models.ManyToManyField(to='organization.organizationpassword'),
        ),
    ]
