from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from vivPets.models import Pet, Species, Variant, Skill
from accounts.models import Player
from django.db.models.aggregates import Count
import random
from random import randint

# Create your views here.
class HomePageView(View):
    template_name = "home.html"
    def dispatch(self, *args, **kwargs):
        num_of_pets = Pet.objects.aggregate(count=Count('id'))['count']
        random_num = random.randint(0, num_of_pets -1)
        random_pet = Pet.objects.all()[random_num]
        random_id = random_pet.pk
        current_user = self.request.user
        if current_user.is_authenticated:
            current_user = self.request.user
            return render(self.request, self.template_name, {"random_pet": random_id})
        else:
            return render(self.request, self.template_name, {"random_pet": random_id})
