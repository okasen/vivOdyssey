from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from vivPets.models import Pet, Species, Variant, Skill
from accounts.models import Player
from user_profiles.models import User_Profile
from django.db.models.aggregates import Count
import random
from random import randint

# Create your views here.
class HomePageView(View):
    template_name = "home.html"
    def dispatch(self, *args, **kwargs):
        num_of_pets = Pet.objects.aggregate(count=Count('id'))['count']
        if num_of_pets > 0:
            random_num = random.randint(0, num_of_pets -1)
            random_pet = Pet.objects.all()[random_num]
            random_pet_id = random_pet.pk
        else:
            random_pet_id = 0

        num_of_profiles = User_Profile.objects.aggregate(count=Count('id'))['count']
        if num_of_profiles > 0:
            random_num = random.randint(0, num_of_profiles -1)
            random_profile = User_Profile.objects.all()[random_num]
            random_profile_id = random_profile.player.pk
        else:
            random_profile_id = 0

        current_user = self.request.user
        if current_user.is_authenticated:
            current_user = self.request.user
            return render(self.request, self.template_name, {"random_pet": random_pet_id, "random_profile": random_profile_id})
        else:
            return render(self.request, self.template_name, {"random_pet": random_pet_id, "random_profile": random_profile_id})
