from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.widgets import DateInput
import datetime

from accounts.models import Player
from viv_pets.models import Pet
# Create your models here.

class User_Profile(models.Model):
    player = models.ForeignKey(Player, unique=True, on_delete=models.CASCADE)
    petLimit = models.IntegerField(default=2)
    friendlyName = models.CharField(max_length=30)
    bio = models.CharField(max_length=500, default="Nothing to see here!", blank=True)
    starredPet = models.ForeignKey(Pet, on_delete=models.PROTECT, blank=True, null=True)
