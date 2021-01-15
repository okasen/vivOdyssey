from django.urls import path
from .views import QAView, AnswerView
from . import views

urlpatterns = [
    path('answer/<int:question_id>/', AnswerView.as_view(), name="answer"),
    path('moderation/', QAView.as_view(), name="moderation"),
    path('answer/all/', views.allQuestions, name='all'),
    path('answer/all-answers/', views.userResults, name='answers'),
    ]
