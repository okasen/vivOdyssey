from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .forms import QuestionCreate
from .models import Question
from django.urls import reverse_lazy
from django.views import View

# Create your views here.

def receiveQuestion(request):
    if request.is_ajax and request.method == "GET":
        question_title = request.GET.get("title", None)
        if Question.objects.filter(title = question_title).exists(): #if the question with this title exists, invalid
            return JsonResponse({"valid":False}, status = 200)
        else:
            return JsonResponse({"valid":True}, status = 200)

    return JsonResponse({}, status = 400)


class QAView(View):
    form_class = QuestionCreate
    template_name = 'user_polls/polls.html'
    def get(self, *args, **kwargs):
        form = self.form_class()
        questions = Question.objects.all()
        return render(self.request, self.template_name, {"form": form, "questions": questions})

    def post(self, *args, **kwargs):
        form_class = QuestionCreate
        if self.request.is_ajax and self.request.method == "POST":
            question = QuestionCreate(self.request.POST)
            if form.is_valid():
                instance = form.save()
                ser_instance = serializers.serialize('json', [ instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error message": form.errors}, status=400)

        return JsonResponse({"error": ""}, status=400)


