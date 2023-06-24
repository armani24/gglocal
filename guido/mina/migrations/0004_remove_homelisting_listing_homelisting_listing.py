# Generated by Django 4.1.7 on 2023-06-24 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_listingcategory_icon_class'),
        ('mina', '0003_homelisting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homelisting',
            name='listing',
        ),
        migrations.AddField(
            model_name='homelisting',
            name='listing',
            field=models.ManyToManyField(to='myapp.listing'),
        ),
    ]