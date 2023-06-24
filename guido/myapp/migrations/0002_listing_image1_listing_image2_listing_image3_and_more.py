# Generated by Django 4.1.5 on 2023-06-15 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image1',
            field=models.ImageField(default=1, upload_to='listing_images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='image2',
            field=models.ImageField(blank=True, upload_to='listing_images/'),
        ),
        migrations.AddField(
            model_name='listing',
            name='image3',
            field=models.ImageField(blank=True, upload_to='listing_images/'),
        ),
        migrations.AddField(
            model_name='listing',
            name='image4',
            field=models.ImageField(blank=True, upload_to='listing_images/'),
        ),
    ]