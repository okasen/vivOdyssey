from django import forms
from django.forms import ModelForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django import forms

from accounts.models import Player

User = get_user_model()

# Register your models here

class CustomUserCreationForm(ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Player
        fields = ('email', 'username', 'Display_Name', 'date_of_birth')
        

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    date_of_birth = forms.DateField(
        widget=forms.DateInput(format='%m/%d/%Y'),
        input_formats=('%m/%d/%Y', ), label="Date of Birth (MM/DD/YYYY)"
        )


class CustomUserChangeForm(ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Player
        fields = ('email', 'username', 'Display_Name', 'date_of_birth', 'is_admin')
        
    def clean_passsword2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2


class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (    
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(Player, UserAdmin)

admin.site.unregister(Group)
