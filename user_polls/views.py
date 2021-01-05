from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .forms import QuestionCreate
from .models import Question
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.

class QAView(generic.CreateView):
    def questionView(request):
        form = QuestionCreate()
        questions = Question.objects.all()
        return render(request, "user_polls/polls.html", {"form": form, "questions": questions})

    def postQuestion(request):
        if request.is_ajax and request.method == "POST":
            question = QuestionCreate(request.POST)
            if form.is_valid():
                instance = form.save()
                ser_instance = serializers.serialize('json', [ instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error message": form.errors}, status=400)

        return JsonResponse({"error": ""}, status=400)

    def receiveQuestion(request):
        if request.is_ajax and request.method == "GET":
            question_title = request.GET.get("title", None)
            if Question.objects.filter(title = title).exists(): #if the question with this title exists, invalid
                return JsonResponse({"valid":False}, status = 200)
            else:
                return JsonResponse({"valid":True}, status = 200)

        return JsonResponse({}, status = 400)
    template_name = 'user_polls/polls.html'
