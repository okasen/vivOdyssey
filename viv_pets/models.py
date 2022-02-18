from django.db import models
from django.utils import timezone

from accounts.models import Player
from profanity.validators import validate_is_profane_nospace


# Create your models here.

class Skill(models.Model):
    class Targets(models.IntegerChoices):
        ONE = 1;
        TWO = 2;
        THREE = 3;
        TEAM = 4;
    class teamTargets(models.IntegerChoices):
        OWN = 1;
        OTHER = 2;
    class Categories(models.IntegerChoices):
        OFFENSIVE = 1;
        DEFENSIVE = 2;
        HEALING = 3;
    name = models.CharField(max_length=30)
    target_team = models.IntegerField(choices = teamTargets.choices)
    target_num = models.IntegerField(choices = Targets.choices)
    damage_num = models.IntegerField()
    defense_mod = models.IntegerField()
    healing_num = models.IntegerField()
    energy_cost = models.IntegerField()
    category = models.IntegerField(choices = Categories.choices)

    def __str__(self):
        return self.name

class Egg(models.Model):
    name = models.CharField(max_length=30)
    flavour_text = models.CharField(max_length=500)
    attack_buff = models.IntegerField()
    defense_buff = models.IntegerField()
    hitpoints_buff = models.IntegerField()
    energy_buff = models.IntegerField()
    eating_effect = models.CharField(max_length=500)

    def __str__(self):
       return self.name

class Species(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    egg = models.OneToOneField(Egg, on_delete=models.PROTECT,)
    base_attack = models.IntegerField()
    base_defense = models.IntegerField()
    base_hitpoints = models.IntegerField()
    base_skills =  models.ManyToManyField('Skill', symmetrical=False)
    base_energy = models.IntegerField()

    def __str__(self):
       return self.name

class Variant(models.Model):
    name = models.CharField(max_length=30)
    species = models.ForeignKey(Species, on_delete=models.PROTECT,)
    attack_modifier = models.IntegerField()
    defense_modifier = models.IntegerField()
    hitpoints_modifier = models.IntegerField()
    energy_modifier = models.IntegerField()
    extra_skills = models.ManyToManyField('Skill', symmetrical=False)

    def __str__(self):
       return self.name

class Pet(models.Model):
    class Gender(models.IntegerChoices):
        FEMALE = 1;
        MALE = 2;
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    date_created = models.DateField(default=timezone.now())
    name = models.CharField(max_length=15, validators=[validate_is_profane_nospace])
    description = models.CharField(max_length=500, blank=True, validators=[validate_is_profane_nospace])
    species = models.ForeignKey(Species, on_delete=models.PROTECT,)
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT,)
    gender = models.IntegerField(choices = Gender.choices)
    hatched = models.BooleanField(default=True)
    attack_modifier = models.IntegerField(blank=True, null=True)
    defense_modifier = models.IntegerField(blank=True, null=True)
    hitpoints_modifier = models.IntegerField(blank=True, null=True)
    energy_modifier = models.IntegerField(blank=True, null=True)
    extra_skills = models.ManyToManyField('Skill', db_column='extra_skills', symmetrical=False, blank=True, null=True)

    def __str__(self):
        return self.name
