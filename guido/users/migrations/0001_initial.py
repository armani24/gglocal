# Generated by Django 4.1.5 on 2023-06-16 13:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Phone number must contain only digits.', regex='^[0-9]*$')])),
                ('is_admin', models.BooleanField(default=False)),
                ('is_customer', models.BooleanField(default=False)),
                ('is_owner', models.BooleanField(default=False)),
                ('is_guid', models.BooleanField(default=False)),
                ('valid_account', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
