# Generated by Django 4.1.5 on 2023-06-18 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_openinghour_listing_opening_hour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='opening_hour',
        ),
        migrations.AddField(
            model_name='listing',
            name='opening_hour',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.openinghour'),
        ),
    ]
