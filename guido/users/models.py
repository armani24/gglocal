from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from PIL import Image
from django.dispatch import receiver


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Normalize email address
        email = self.normalize_email(email)
        
        # Create a new user instance
        user = self.model(email=email, **extra_fields)
        
        # Set the password if provided
        user.set_password(password)
        
        # Save the user in the database
        user.save()
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Create a new user with admin privileges
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_customer', False)
        extra_fields.setdefault('is_owner', False)
        extra_fields.setdefault('valid_account', True)
        
        return self.create_user(email, password, **extra_fields)

def get_image_filename(instance, filename):
    is_customer = instance.user.is_customer
    is_owner = instance.user.is_owner
    is_guid = instance.user.is_guid
    if is_customer:
        user = instance.user.email
        i = "profile/customer/%s" %  user
        return '/'.join([i, filename])
    if is_owner:
        user = instance.user.email
        i = "profile/owner/%s" %  user
        return '/'.join([i, filename])
    if is_guid:
        user = instance.user.email
        i = "profile/guide/%s" %  user
        return '/'.join([i, filename])
    else:
        return None


class MyUser(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^[0-9]*$', message="Phone number must contain only digits.")
    phone = models.CharField(max_length=20, validators=[phone_regex])
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_guid = models.BooleanField(default=False)
    valid_account = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
        
    def is_staff(self, perm, obj=None):
        return self.is_admin

class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    image = models.ImageField(default='1.png', upload_to=get_image_filename)

    def __str__(self):
        return f'{self.user.email} Profile'
    #def customer_profile(self, *args, **kwargs):

    def save(self):
        super().save()

        img = Image.open(self.image.path) # for profile
        output_size = (600, 600)
        img = img.resize((530,285))
        img.save(self.image.path)


import os

@receiver(models.signals.post_save, sender=MyUser, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()

@receiver(models.signals.pre_save, sender=Profile)
def auto_delete_product_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file_f = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file_f = instance.image


@receiver(models.signals.post_delete, sender=Profile)
def auto_delete_product_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)



