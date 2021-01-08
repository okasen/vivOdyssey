from django import forms
from django.forms import ModelForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django import forms

from accounts.models import Player

User = get_user_model()

# Register your models here


admin.site.register(Player)
