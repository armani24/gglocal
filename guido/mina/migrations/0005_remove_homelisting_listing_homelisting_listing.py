# Generated by Django 4.1.7 on 2023-06-24 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_listingcategory_icon_class'),
        ('mina', '0004_remove_homelisting_listing_homelisting_listing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homelisting',
            name='listing',
        ),
        migrations.AddField(
            model_name='homelisting',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.listing'),
        ),
    ]
