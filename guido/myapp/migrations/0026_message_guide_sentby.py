# Generated by Django 4.1.7 on 2023-06-22 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_message_guide_o_receiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='message_guide',
            name='sentby',
            field=models.CharField(choices=[('customer', 'customer'), ('guide', 'guide'), ('owner', 'owner')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]