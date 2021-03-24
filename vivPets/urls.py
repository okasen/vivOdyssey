from django.urls import path

from .views import ModPetView, UserPetsView, ViewPet

urlpatterns = [
	path('moderation/', ModPetView.as_view(), name='moderate-pets'),
	path('', UserPetsView.as_view(), name='user-pets'),
	path('userpets/<int:pet_id>/', ViewPet.as_view(), name='view-pet'),
]
