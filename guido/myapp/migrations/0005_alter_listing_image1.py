# Generated by Django 4.1.5 on 2023-06-16 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_listing_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image1',
            field=models.ImageField(blank=True, upload_to='listing_images/'),
        ),
    ]