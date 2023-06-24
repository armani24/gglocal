from django.db import models
from django.dispatch import receiver
import os

from django.utils.text import slugify
from users.models import MyUser

from django.core.validators import RegexValidator
from PIL import Image, ImageDraw

class ListingCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    svg_img = models.CharField(max_length=50, null=True, blank=True)
    icon_class = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically generate slug from the name
        self.slug = slugify(self.name)
        if self.svg_img:
            self.svg_img = "/static/myapp/images/icons/%s" % self.svg_img
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    city_img = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if self.city_img:
            self.city_img = "/static/myapp/images/cities/%s" % self.city_img
    
        super().save(*args, **kwargs)
   

class Highlight(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

def get_image_filename(instance, filename):
    name = instance.name
    user = instance.author.email
    prod_id = instance.id

    i = "owner/%s/%s/listing/" % (user, name)
    return '/'.join([i, filename])

phone_regex = RegexValidator(regex=r'^[0-9]*$', message="Phone number must contain only digits.")

class Listing(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        ListingCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image1 = models.ImageField(upload_to=get_image_filename)
    image2 = models.ImageField(upload_to=get_image_filename)
    image3 = models.ImageField(upload_to=get_image_filename)
    image4 = models.ImageField(upload_to=get_image_filename)
    is_guide_listing = models.BooleanField(default=False)
    
    phone = models.CharField(max_length=20, validators=[phone_regex], blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    author = models.ForeignKey(
        MyUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    

    highlights = models.ManyToManyField(Highlight)



    def __str__(self):
        return self.name
    
    def save(self):
        super().save()

        img_f = Image.open(self.image1.path)
        img_s = Image.open(self.image2.path)
        img_l = Image.open(self.image3.path)
        img_fr = Image.open(self.image4.path)
        wat = img_f.copy()
        draw = ImageDraw.Draw(wat)
        draw.text((0, 0), 'Guido', (0,0,0))
        img_f = wat
        output_size = (716, 456)
        img_f = img_f.resize(output_size)
        img_s = img_s.resize(output_size)
        img_l = img_l.resize(output_size)
        img_fr = img_fr.resize(output_size)
        print(img_s)
        img_f.save(self.image1.path)
        img_s.save(self.image2.path)
        img_l.save(self.image3.path)
        img_fr.save(self.image4.path)

@receiver(models.signals.post_delete, sender=Listing)
def auto_delete_product_on_delete(sender, instance, **kwargs):
    if instance.image1 and instance.image2 and instance.image3 and instance.image4:
        if os.path.isfile(instance.image1.path) and os.path.isfile(instance.image2.path) and os.path.isfile(instance.image3.path) and os.path.isfile(instance.image4.path):
            os.remove(instance.image1.path)
            os.remove(instance.image2.path)
            os.remove(instance.image3.path)
            os.remove(instance.image4.path)


@receiver(models.signals.pre_save, sender=Listing)
def auto_delete_product_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file_f = sender.objects.get(pk=instance.pk).image1
        old_file_s = sender.objects.get(pk=instance.pk).image2
        old_file_l = sender.objects.get(pk=instance.pk).image3
        old_file_fr = sender.objects.get(pk=instance.pk).image4
    except sender.DoesNotExist:
        return False

    new_file_f = instance.image1
    new_file_s = instance.image2
    new_file_l = instance.image3
    new_file_fr = instance.image4


    

class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Messages(models.Model):
    customer = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    message = models.CharField(max_length=200)
    o_receiver = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)
    viewed = models.BooleanField(default=False)

def guide_image_filename(instance, filename):
    name = instance.name
    user = instance.author.email
    prod_id = instance.id

    i = "guide/%s/%s/listing/" % (user, name)
    return '/'.join([i, filename])


class Guides(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(MyUser,on_delete=models.SET_NULL,null=True,blank=True)
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image1 = models.ImageField(upload_to=guide_image_filename)
    phone = models.CharField(max_length=20, validators=[phone_regex], blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    approved = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
    def save(self):
        super().save()

        img_f = Image.open(self.image1.path)
        wat = img_f.copy()
        draw = ImageDraw.Draw(wat)
        draw.text((0, 0), 'Guido', (0,0,0))
        img_f = wat
        output_size = (716, 456)
        img_f = img_f.resize(output_size)
        img_f.save(self.image1.path)

@receiver(models.signals.post_delete, sender=Guides)
def auto_delete_product_on_delete(sender, instance, **kwargs):
    if instance.image1:
        if os.path.isfile(instance.image1.path):
            os.remove(instance.image1.path)


@receiver(models.signals.pre_save, sender=Guides)
def auto_delete_product_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file_f = sender.objects.get(pk=instance.pk).image1
    except sender.DoesNotExist:
        return False

    new_file_f = instance.image1


class GuidesReview(models.Model):
    guides = models.ForeignKey(Guides, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Message_Guide(models.Model):
    """ msg sent to all part """
    sentby = (
        ('customer','customer'),
        ('guide','guide'),
        ('owner','owner')
    )
    customer = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    message = models.CharField(max_length=200)
    guide_info = models.ForeignKey(Guides, on_delete=models.SET_NULL, null=True)
    o_receiver = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)
    viewed = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    sentby = models.CharField(max_length=10)



# admin controlled models
