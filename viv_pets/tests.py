import datetime
import json

from django.contrib.auth.models import Group
from django.test import TestCase, Client

from accounts.models import Player
from viv_pets.models import Pet, Species, Variant, Skill, Egg


class TestPets(TestCase):
    def setUp(self):
        self.player = Player.objects.create_user(username="test",
                                            email="test@email.net",
                                            password="test_pass",)

        group = Group(name="moderators")
        group.save()
        self.player.groups.add(group)
        self.player.save()

        base_egg = Egg.objects.create(name="mock egg",
                                      flavour_text="This is a mock egg",
                                      attack_buff=1,
                                      defense_buff=1,
                                      hitpoints_buff=1,
                                      energy_buff=1,
                                      eating_effect=1)
        base_egg.save()

        self.mock_species = Species.objects.create(name="mockspecies",
                                         description="mock describe",
                                         egg=base_egg,
                                         base_attack=1,
                                         base_defense=1,
                                         base_hitpoints=1,
                                         base_energy=1)

        self.mock_species.save()

        self.mock_variant = Variant.objects.create(name="mockvar",
                                         species=self.mock_species,
                                         attack_modifier=1,
                                         defense_modifier=1,
                                         hitpoints_modifier=1,
                                         energy_modifier=1)

        self.mock_variant.save()

        self.mock_pet = Pet.objects.create(owner=self.player,
                                           date_created=datetime.datetime.now(tz=datetime.timezone.utc),
                                           name="Friend",
                                           description="A friend",
                                           species=self.mock_species,
                                           variant=self.mock_variant,
                                           gender=2,
                                           hatched=True,
                                           attack_modifier=1,
                                           defense_modifier=1,
                                           hitpoints_modifier=1,
                                           energy_modifier=1,
                                           )

        self.mock_pet.save()

        self.client = Client()
        self.client.login(username="test", password="test_pass")

    def test_bad_word_in_pet_name_yields_error(self):
        profane_pet = self.mock_pet
        profane_pet.name = "Fuck"
        pet_data = {"name": profane_pet.name,
                    "date_created": "12/12/2022",
                    "description": profane_pet.description,
                    "species": profane_pet.species.pk,
                    "variant": profane_pet.variant.pk,
                    "gender": profane_pet.gender,
                    "attack_modifier": profane_pet.attack_modifier,
                    "defense_modifier": profane_pet.defense_modifier,
                    "energy_modifier": profane_pet.energy_modifier,
                    "hitpoints_modifier": profane_pet.hitpoints_modifier
                    }

        response = self.client.post("/pets/new/", data=pet_data, follow=True)
        assert "error" in json.loads(response.content)

    def test_bad_word_in_description_yields_error(self):
        profane_pet = self.mock_pet
        profane_pet.description = "Fuck"
        pet_data = {"name": profane_pet.name,
                    "date_created": "12/12/2022",
                    "description": profane_pet.description,
                    "species": profane_pet.species.pk,
                    "variant": profane_pet.variant.pk,
                    "gender": profane_pet.gender,
                    "attack_modifier": profane_pet.attack_modifier,
                    "defense_modifier": profane_pet.defense_modifier,
                    "energy_modifier": profane_pet.energy_modifier,
                    "hitpoints_modifier": profane_pet.hitpoints_modifier
                    }
        response = self.client.post("/pets/new/", data=pet_data, follow=True)
        assert "error" in json.loads(response.content)

    def test_profane_name_errors_modview(self):
        profane_pet = self.mock_pet
        profane_pet.name = "Fuck"
        pet_data = {"owner": self.player.pk,
                    "date_created": "12/12/2022",
                    "name": profane_pet.name,
                    "description": profane_pet.description,
                    "species": self.mock_species.pk,
                    "variant": self.mock_variant.pk,
                    "gender": profane_pet.gender,
                    "attack_modifier": profane_pet.attack_modifier,
                    "defense_modifier": profane_pet.defense_modifier,
                    "energy_modifier": profane_pet.energy_modifier,
                    "hitpoints_modifier": profane_pet.hitpoints_modifier}

        response = self.client.post("/pets/moderation/", data=pet_data)
        assert "error" in json.loads(response.content)

    def test_profane_description_errors_modview(self):
        profane_pet = self.mock_pet
        profane_pet.description = "Fuck"
        pet_data = {"owner": self.player.pk,
                    "date_created": "12/12/2022",
                    "name": profane_pet.name,
                    "description": profane_pet.description,
                    "species": self.mock_species.pk,
                    "variant": self.mock_variant.pk,
                    "gender": profane_pet.gender,
                    "attack_modifier": profane_pet.attack_modifier,
                    "defense_modifier": profane_pet.defense_modifier,
                    "energy_modifier": profane_pet.energy_modifier,
                    "hitpoints_modifier": profane_pet.hitpoints_modifier}

        response = self.client.post("/pets/moderation/", data=pet_data)
        assert "error" in json.loads(response.content)

    def test_false_positive_name_doesnt_error(self):
        profane_pet = self.mock_pet
        profane_pet.name = "basement"
        pet_data = {"name": profane_pet.name,
                    "date_created": "12/12/2022",
                    "description": profane_pet.description,
                    "species": profane_pet.species.pk,
                    "variant": profane_pet.variant.pk,
                    "gender": profane_pet.gender,
                    "attack_modifier": profane_pet.attack_modifier,
                    "defense_modifier": profane_pet.defense_modifier,
                    "energy_modifier": profane_pet.energy_modifier,
                    "hitpoints_modifier": profane_pet.hitpoints_modifier
                    }
        response =self.client.post("/pets/new/", data=pet_data, follow=True)
        assert response.status_code == 200

    def test_false_positive_description_doesnt_error(self):
        profane_pet = self.mock_pet
        profane_pet.description = "basement"
        pet_data = {"name": profane_pet.name,
                    "date_created": "12/12/2022",
                    "description": profane_pet.description,
                    "species": profane_pet.species.pk,
                    "variant": profane_pet.variant.pk,
                    "gender": profane_pet.gender,
                    "attack_modifier": profane_pet.attack_modifier,
                    "defense_modifier": profane_pet.defense_modifier,
                    "energy_modifier": profane_pet.energy_modifier,
                    "hitpoints_modifier": profane_pet.hitpoints_modifier
                    }
        response = self.client.post("/pets/new/", data=pet_data, follow=True)
        assert response.status_code == 200
