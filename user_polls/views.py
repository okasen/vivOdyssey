from django import template
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core import serializers
from .forms import QuestionCreate, AnswerForm
from .models import Question, Answer
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import _datetime
from django.utils import timezone
from accounts.models import Player

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
register = template.Library()


# Create your views here.

def allQuestions(request):
    questions = Question.objects.all()
    return render(request, 'user_polls/polls/list.html', {"questions": questions})

def userResults(request, *args, **kwargs):
    answers = Answer.objects.all()
    questions = Question.objects.all()
    listOfQuestions = []
    listOfTitles = []
    context = dict()

    for question in questions:
        if question.pk not in listOfQuestions:
            listOfQuestions.append(question.pk)

    for qid in listOfQuestions:
        qidList = answers.filter(question = qid)
        qidQuestion = questions.get(pk = qid)
        context[qidQuestion.title] = qidList

    return render(request, 'user_polls/polls/answers_given.html', {'qAndAs': context})

class AnswerView(View): #view for answering questions
    atemplate_name = 'user_polls/polls/answer.html'
    form_class = AnswerForm
    questions = Question.objects.all()
    question_id = None
    def get(self, *args, **kwargs):
        form = self.form_class()
        self.question_id = kwargs.get("question_id")
        question = get_object_or_404(Question, pk = self.question_id)
        return render(self.request, self.atemplate_name, {"form": form, "question": question})

    def post(self, *args, **kwargs):
        logger.info('posting')
        if self.request.is_ajax and self.request.method == "POST":
            self.question_id = kwargs.get("question_id")
            answerGiven = self.request.POST['answer']
            questionAnswered = get_object_or_404(self.questions, pk = self.question_id)
            userPk = self.request.user.pk
            userAnswering = Player.objects.get(pk=userPk)
            form = Answer(answer=answerGiven, date_answered=timezone.now(), question=questionAnswered, user=userAnswering)
            if True:
                logger.info('valid')
                form.save()
                return JsonResponse({"answer": answerGiven}, status=200)
            else:
                return JsonResponse({"error": "oh no, but we knew to post"}, status=400)
        else:
                return JsonResponse({"error": "no ajax"}, status=400)


def receiveQuestion(request):
    if request.is_ajax and request.method == "GET":
        question_title = request.GET.get("title", None)
        if Question.objects.filter(title = question_title).exists(): #if the question with this title exists, invalid
            return JsonResponse({"valid":False}, status = 200)
        else:
            return JsonResponse({"valid":True}, status = 200)

    return JsonResponse({}, status = 400)

class QAView(UserPassesTestMixin, View): #Question Add View

    def test_func(self):
        return self.request.user.groups.filter(name = "moderators")

    form_class = QuestionCreate
    model_class = Question
    qtemplate_name = 'user_polls/polls/moderation.html'
    def get(self, *args, **kwargs):
        form = self.form_class()
        questions = Question.objects.all()
        return render(self.request, self.qtemplate_name, {"form": form, "questions": questions})

    def post(self, *args, **kwargs):
        logger.debug('We know to do something')
        # request should be ajax and method should be POST.
        if self.request.is_ajax and self.request.method == "POST":
            requestType = self.request.headers['reqType']
            if requestType == "Post":
                # get the form data
                form = self.form_class(self.request.POST)
                # save the data and after fetch the object in instance
                if form.is_valid():
                    instance = form.save()
                    form.save()
                    ser_instance = serializers.serialize('json', [ instance, ])
                    return JsonResponse({"instance": ser_instance}, status=200)
                else:
                    return JsonResponse({"error": "oh no, but we knew to post new Q"}, status=400)
            elif requestType == "Delete":
                qClass = self.model_class()
                qid = self.request.POST.get('delId', None)
                getId = get_object_or_404(Question, title = qid)
                getId.delete()
                deleted = { 'deleted' : qid }
                return JsonResponse(deleted, status=200)
            else:
                return JsonResponse({"error": "couldn't discern type"}, status=400)
