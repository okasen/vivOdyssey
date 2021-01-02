from django.urls import path

from .views import LoreView

urlpatterns = [
	path('lore', LoreView.readLore, name='about'),
]
