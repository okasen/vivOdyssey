from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.forms.widgets import DateInput
import datetime


# Create your models here.

class Player(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    username = models.CharField(max_length=200,unique=True)
    date_of_birth = models.DateField(("Date of birth (mm/dd/yyyy)"), default=datetime.date.today)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
