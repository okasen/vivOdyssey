from django.urls import path

from .views import GameView

urlpatterns = [
	path('fishing/', GameView.as_view(), name='playfishing'),
]
