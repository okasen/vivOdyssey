from django.urls import path
from .views import QAView
from QAView import receiveQuestion

urlpatterns = [
    path('polls/', QAView.as_view(), name="polls"),
    path('get/ajax/validate/question', QAView.receiveQuestion, name = "receive_Question"),
]
