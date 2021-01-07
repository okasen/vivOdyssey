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
    model_class = Question
    template_name = 'user_polls/polls.html'
    def get(self, *args, **kwargs):
        form = self.form_class()
        questions = Question.objects.all()
        return render(self.request, self.template_name, {"form": form, "questions": questions})

    def post(self, *args, **kwargs):
        # request should be ajax and method should be POST.
        if self.request.is_ajax and self.request.method == "POST":
            requestType = self.request.POST['reqType']
            if requestType == "Post":
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
            elif requestType == "Delete":
                qClass = self.model_class()
                qid = self.request.POST.get('delId', None)
                getId = get_object_or_404(Question, title = qid)
                Question.objects.title.filter(title=getId).delete()
                qClass.save()
                deleted =  { 'deleted' : qid }
                return JsonResponse(deleted, status=200)
            else:
                return JsonResponse({"error": "couldn't discern type"}, status=400)
            
            


