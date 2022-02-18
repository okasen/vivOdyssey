from django import forms

from .models import Pet


class PetCreate(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        super(PetCreate, self).__init__(*args, **kwargs)

    class Meta:
        model = Pet
        fields = ("__all__")

class UserPetCreate(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        super(UserPetCreate, self).__init__(*args, **kwargs)

    class Meta:
        model = Pet
        fields = ("name","description","species","variant","gender","attack_modifier","defense_modifier","energy_modifier","hitpoints_modifier")