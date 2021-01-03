from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http import HttpResponse
import os


# Create your views here.
class LoreView(TemplateView):

    def readLore(request):
        textFile = "text/BackStory.txt"
        textFilePath = os.path.join(settings.STATIC_URL, textFile)
        try:
            with open(textFilePath, 'r') as f:
                loreText = f.read()
            context = {'loreContents' : loreText }
        except:
            context = {'loreContnets' : "stuff" }
        return render(request, 'lore/about.html', context, content_type="text/html")
