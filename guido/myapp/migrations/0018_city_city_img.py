# Generated by Django 4.1.7 on 2023-06-21 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_listingcategory_svg_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='city_img',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]