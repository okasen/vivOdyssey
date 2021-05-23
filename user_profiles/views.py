from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User_Profile
from vivPets.models import Pet
from accounts.models import Player

# Create your views here.

#A view for viewing your own user user_profile

#a view for viewing other people's profiles

def create_missing_profile(user, **kwargs):
    newProfile = User_Profile(player = user.id, friendlyName = player.username)
    newProfile.save()

class ViewOwnProfile(LoginRequiredMixin, View):
    template_name = "user_profiles/profile.html"
    def get(self, *args, **kwargs):
        current_user = self.request.user
        if User_Profile.objects.filter(player = current_user.id) == 0: #if there's not a profile for this user
            create_missing_profile(current_user)
        current_profile = get_object_or_404(User_Profile, player = current_user.id)
        pets = Pet.objects.filter(owner = current_user)
        return render(self.request, self.template_name, {"current_profile" : current_profile, "pets": pets})

class ViewOtherProfile(View):
    template_name = "user_profiles/profile.html"

    def get(self, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = get_object_or_404(Player, pk = user_id)
        if User_Profile.objects.filter(player = user.id) == 0: #if there's not a profile for this user
            create_missing_profile(user)
        current_profile = get_object_or_404(User_Profile, player = user_id)
        pets = Pet.objects.filter(owner = user)
        return render(self.request, self.template_name, {"current_profile" : current_profile, "pets": pets})
