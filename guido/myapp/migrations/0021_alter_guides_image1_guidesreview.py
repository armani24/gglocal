# Generated by Django 4.1.7 on 2023-06-22 09:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0020_guides_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guides',
            name='image1',
            field=models.ImageField(upload_to=myapp.models.guide_image_filename),
        ),
        migrations.CreateModel(
            name='GuidesReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('guides', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.guides')),
            ],
        ),
    ]
