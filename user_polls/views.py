from django.shortcuts import render, get_object_or_404
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
        # request should be ajax and method should be POST.
        if self.request.is_ajax and self.request.method == "POST":
            # get the form data
            form = self.form_class(self.request.POST)
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                # serialize in new friend object in json
                ser_instance = serializers.serialize('json', [ instance, ])
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        return JsonResponse({"error": ""}, status=400)

    def delete(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "DELETE":
            form = self.form_class(self.request.POST)
            id = self.request.POST['id']
            getId = get_object_or_404(Question, title = id)
            form.objects.filter(title=getId).delete()            
            
            


