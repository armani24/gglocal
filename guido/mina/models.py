from django.db import models
from django.dispatch import receiver
import os
from PIL import Image, ImageDraw
# Create your models here.
from myapp.models import Listing


def path_filename(instance, filename):
    i = "homeslider/"
    '/'.join([i, filename])

class HomeSlider(models.Model):
    image1 = models.ImageField(upload_to="homeslider/")
    active = models.BooleanField(default=False)


@receiver(models.signals.pre_save, sender=HomeSlider)
def auto_delete_product_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file_f = sender.objects.get(pk=instance.pk).image1
    except sender.DoesNotExist:
        return False

    new_file_f = instance.image1


@receiver(models.signals.post_delete, sender=HomeSlider)
def auto_delete_product_on_delete(sender, instance, **kwargs):
    if instance.image1:
        if os.path.isfile(instance.image1.path):
            os.remove(instance.image1.path)



class HomeListing(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.listing.name

class ContactUs_info(models.Model):
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    active = models.BooleanField(default=False)

    

class AboutUS(models.Model):
    title = models.CharField(max_length=100)
    intoduction = models.CharField(max_length=100)
    description = models.TextField()
