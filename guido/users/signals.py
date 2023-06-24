from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Profile, MyUser
import os


"""
@receiver(post_save, sender=MyUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance.username)
    else:
        #print('--->not found', created)
#@shopowner_required
@receiver(post_save, sender=MyUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

"""


@receiver(pre_save, sender=Profile)
def auto_delete_image_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(instance.image.path):
            os.remove(old_file.path)

    r = []
    k = []
    r.append(new_file.path)
    k.append(old_file.path)

    if k != r:
        try:
            for i in k:
                if i not in r:
                    os.remove(i)
        except:
            pass