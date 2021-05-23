from django.db.models.signals import post_save
from .models import Player
from django.dispatch import receiver
from user_profiles.models import User_Profile

@receiver(post_save, sender=Player)
def create_profile(sender, instance, created, **kwargs):
    if created:
        newProfile = User_Profile(player = instance, friendlyName = instance.username)
        newProfile.save()
