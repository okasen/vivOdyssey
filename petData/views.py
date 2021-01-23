from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.views import View

# Create your views here.
from .models import Pet
from .serializers import PetSerializer

class GetPet(View):
    ptemplate_name = 'petData/pet-home.html'
    def get(self, *args, **kwargs):
        self.data = Pet.objects.all()
        self.context = dict()
        self.context['results'] = self.data
        if self.request.method == 'GET':
            self.serializer = PetSerializer(self.data, many=True)
            return render(self.request, self.ptemplate_name, self.context)
            #Does this really need safe = false?
