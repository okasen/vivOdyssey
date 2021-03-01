from .models import Pet, Variant, Species, Egg, Skill
from django import forms
from django.utils import timezone

class PetCreate(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        super(PetCreate, self).__init__(*args, **kwargs)

    class Meta:
        model = Pet
        fields = ("__all__")

        
