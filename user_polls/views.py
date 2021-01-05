from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .forms import QuestionCreate
from .models import Question
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.

class QAView(generic.CreateView):

    template_name = 'user_polls/polls.html'
