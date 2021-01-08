from django.urls import path
from .views import QAView, AnswerView

urlpatterns = [
    path('moderation/', QAView.as_view(), name="moderation"),
    path('answer/', AnswerView.as_view(), name="answer"),
]
