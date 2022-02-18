# import the logging library
import logging

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from .forms import PetCreate, UserPetCreate
from .models import Pet, Species, Variant, Skill
from profanity.extras import ProfanityFilter

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserPetsMaker(LoginRequiredMixin, View):
    form_class = UserPetCreate
    template_name = "pets/makepet.html"
    form = form_class()
    variants = Variant.objects.all()
    listOfBaseVariants = []  # a list of one variant per species
    listOfSpecies = []
    for variant in variants:
        if variant.species not in listOfSpecies:
            listOfSpecies.append(variant.species)
            listOfBaseVariants.append([variant, variant.species])  # only append a variant if the species hasn't had a variant added yet

    def get(self, *args, **kwargs):  # get all pet types available with one variant displayed
        return render(
            self.request,
            self.template_name,
            {"form": self.form, "species": self.listOfBaseVariants, "pet_errors": []}
        )

    def post(self, *args, **kwargs):
        logger.debug('trying to post a user-made pet')
        pet_errors = []
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            try:
                new_pet = form.save(commit=False)
                new_pet.owner = self.request.user
                pet_modifiers_total = new_pet.attack_modifier + new_pet.defense_modifier + new_pet.hitpoints_modifier + new_pet.energy_modifier
                modifier_goal = 2
                logger.debug('checking for stat validity')
                if pet_modifiers_total != modifier_goal:
                    pet_errors.append("Your pet must have exactly two modifier points distributed across its stats")
                if len(pet_errors) > 0:
                    logger.debug(str(len(pet_errors)) + "errors")
                    return render(self.request, self.template_name, {"form": self.form, "species": self.listOfBaseVariants, "pet_errors": pet_errors, "pet": None})
                elif len(pet_errors) == 0:
                    logger.debug("no errors")
                    context = dict()
                    new_pet.save()
                    return render(self.request, self.template_name, {"form": self.form, "species": self.listOfBaseVariants, "pet_errors": pet_errors, "pet": new_pet})
            except ValueError as e:
                pet_errors.append(
                    "Please ensure there are no errors or profane words in these fields:")
                for error in form.errors:
                    pet_errors.append(error)
                return JsonResponse({"error": pet_errors})


        else:
            pet_errors.append("something went wrong creating this pet! Please report this error to the site admin or a moderator.")
            return render(self.request, self.template_name, {"form": self.form, "species": self.listOfBaseVariants, "pet_errors": pet_errors, "pet": None})


class ViewPet(View):
    template_name = "pets/view.html"
    def get(self, *args, **kwargs):
        self.pet_id = kwargs.get("pet_id")
        pet = get_object_or_404(Pet, pk = self.pet_id)
        species_skills = [skill for skill in Skill.objects.all() if skill in pet.species.base_skills.all()]
        variant_skills = [skill for skill in Skill.objects.all() if skill in pet.variant.extra_skills.all()]
        individual_skills = [skill for skill in Skill.objects.all() if skill in pet.extra_skills.all()]
        stats = dict()
        stats["attack"] = pet.species.base_attack + pet.variant.attack_modifier + (pet.attack_modifier or 0)
        stats["defense"] = pet.species.base_defense + pet.variant.defense_modifier + (pet.defense_modifier or 0)
        stats["hitpoints"] = pet.species.base_hitpoints + pet.variant.hitpoints_modifier + (pet.hitpoints_modifier or 0)
        stats["energy"] = pet.species.base_energy + pet.variant.energy_modifier + (pet.energy_modifier or 0)
        skills = species_skills + variant_skills + individual_skills
        gender = pet.get_gender_display()
        return render(self.request, self.template_name, {"pet": pet, "skills": skills, "stats": stats, "gender": gender})

class UserPetsView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        current_user = self.request.user
        currentUserId = current_user.id
        pets = Pet.objects.filter(owner = currentUserId)
        template_name = "pets/userpets.html"
        return render(self.request, template_name, {"user": current_user.username, "pets": pets})


# view for moderators to add pets
class ModPetView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="moderators")

    form_class = PetCreate
    model_class = Pet
    pets = Pet.objects.all()
    availSpecies = Species.objects.all()
    availVariants = Variant.objects.all()
    context = dict()
    template_name = "pets/moderation.html"

    def get(self, *args, **kwargs):
        logger.debug("getting list of species")
        form = self.form_class()
        listOfSpecies = []

        for species in self.availSpecies:
            if species.pk not in listOfSpecies:
                listOfSpecies.append(species.pk)

        for speciesPk in listOfSpecies:
            variantList = self.availVariants.filter(species = speciesPk)
            species = self.availSpecies.get(pk = speciesPk) #gives the human readable name of the species
            self.context[species.name] = variantList #get a list of variants by each species

        return render(self.request, self.template_name, {"form": form, "pets": self.pets, 'speciesAndVariants': self.context}, content_type="text/html")

    def post(self, *args, **kwargs):
        logger.debug('trying to post a pet')
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if form.is_valid():
                print('form is valid')
                #TODO: make it so you can't make naughty pets with sweary names
                #TODO: check that the species/variant combo is valid
                instance = form.save()
                context = dict()
                context["response"] = instance
                form.save()
                return render(self.request, self.template_name, context)

            else:
                return JsonResponse({"error": "Oh no, something went wrong POSTing this pet",
                                     "form errors": form.errors})


#TODO make a view for hatching pets?

#TODO make a view for breeding pets
