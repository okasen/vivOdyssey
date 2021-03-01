from django.urls import path

from .views import ModPetView, UserPetsView

urlpatterns = [
	path('moderation/', ModPetView.as_view(), name='moderate-pets'),
	path('userpets/', UserPetsView.as_view(), name='user-pets'),
]
