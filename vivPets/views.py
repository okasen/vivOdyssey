from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.urls import reverse_lazy, reverse
from .forms import PetCreate
from .models import Pet, Species, Variant
from accounts.models import Player

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
#
# Create your views here.
#
# TODO make a view to see all the pets you have
#
# TODO make a view for acquiring pets
#
# view for moderators to add pets
class UserPetsView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        current_user = self.request.user
        currentUserId = current_user.id
        pets = Pet.objects.filter(owner = currentUserId)
        template_name = "pets/userpets.html"
        return render(self.request, template_name, {"user": current_user.username, "pets": pets})


class ModPetView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.groups.filter(name = "moderators")

    form_class = PetCreate
    model_class = Pet
    pets = Pet.objects.all()
    availSpecies = Species.objects.all()
    availVariants = Variant.objects.all()
    context = dict()
    template_name = "pets/moderation.html"

    def get(self, *args, **kwargs):
        logger.debug("getting")
        form = self.form_class()
        listOfSpecies = []
        listOfVariants = []

        for species in self.availSpecies:
            if species.pk not in listOfSpecies:
                listOfSpecies.append(species.pk)

        for speciesPk in listOfSpecies:
            variantList = self.availVariants.filter(species = speciesPk)
            species = self.availSpecies.get(pk = speciesPk) #gives the human readable name of the species
            self.context[species.name] = variantList #get a list of variants by each species

        return render(self.request, self.template_name, {"form": form, "pets": self.pets, 'speciesAndVariants': self.context}, content_type="text/html")

    def post(self, *args, **kwargs):
        logger.debug('inside post')
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if form.is_valid():
                logger.debug('form is valid')
                #TODO: make it so you can't make naughty pets with sweary names
                #TODO: check that the species/variant combo is valid
                instance = form.save()
                form.save()
                return HttpResponseRedirect(reverse("moderate-pets"))
            else:
                return JsonResponse({"error": "Oh no, something went wrong POSTing this pet"})


#TODO make a view for hatching pets?

#TODO make a view for breeding pets
