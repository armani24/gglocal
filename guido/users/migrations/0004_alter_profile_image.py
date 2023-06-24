# Generated by Django 4.1.7 on 2023-06-22 11:11

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='1.png', upload_to=users.models.get_image_filename),
        ),
    ]
