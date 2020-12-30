from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm Password', widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
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
