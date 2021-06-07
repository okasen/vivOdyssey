from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.forms.widgets import DateInput
import datetime
from django.utils import timezone
from profanity.validators import validate_is_profane_nospace


# Create your models here.

class Player(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    username = models.CharField(max_length=18,unique=True,validators=[validate_is_profane_nospace])
    date_of_birth = models.DateField(("Date of birth (mm/dd/yyyy)"), default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
