# django doc recommends using own file instead of models.py

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User) #signal, sender  - when a user is saved send this signal  which is then recieved by this reciever decorator
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) # create Profile object when user is created


@receiver(post_save, sender=User) #signal, sender  - when a user is saved send this signal  which is then recieved by this reciever decorator
def save_profile(sender, instance, **kwargs):
        instance.profile.save()
