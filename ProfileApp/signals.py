from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# This is a signal that will be sent when a new user is created, it will create a profile for that user
@receiver(post_save, sender=User)
def newUser(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

