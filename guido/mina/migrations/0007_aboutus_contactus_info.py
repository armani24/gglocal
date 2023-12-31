# Generated by Django 4.1.7 on 2023-06-24 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mina', '0006_alter_homelisting_listing'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('intoduction', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ContactUs_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]
