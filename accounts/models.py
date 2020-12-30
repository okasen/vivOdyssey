from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.forms.widgets import DateInput


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        if not email:
            raise ValueError('The given email must be set')
        if not Username:
            raise ValueError('You must set a unique username')
        birthdate = self.cleaned_date['date_of_birth']
        today = date.today()
        if (birthdate.year + 13, birthdate.month, birthdate.day) > (today.year, toay.month, today.day):
            raise ValueError('You must be at least 13 years old to join.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, date_of_birth, **extra_fields):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class Player(AbstractUser):
##    email = models.EmailField(_('email address'), unique=True)
##    Username = models.CharField(max_length=40, unique=True)
##    USERNAME_FIELD = 'Username'
    Display_Name = models.CharField(max_length=40, unique=False)
    date_of_birth = models.DateField()
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    about_user = models.TextField(max_length=200, blank=True) #user bio section
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['date_of_birth', 'EMAIL_FEILD']

