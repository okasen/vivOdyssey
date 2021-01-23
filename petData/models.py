from django.db import models

# Create your models here.
class Pet(models.Model):
    species = models.CharField(max_length=150)
    name = models.CharField(max_length=100)
