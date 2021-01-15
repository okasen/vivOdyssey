from django.shortcuts import render
from django.views.generic.base import TemplateView
from accounts.models import Player

# Create your views here.
class GameView(TemplateView):

    template_name = "fishing/fishing-game.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_player'] = self.request.user
        return context
