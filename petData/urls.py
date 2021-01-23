from django.urls import path

from .views import GetPet

urlpatterns = [
	path('your-pets/', GetPet.as_view(), name='userpets'),
]
