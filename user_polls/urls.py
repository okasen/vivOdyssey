from django.urls import path

from .views import QAView

urlpatterns = [
    path('polls/', QAView.as_view(), name="polls"),]
    path('get/ajax/validate/question', QAView.receiveQuestion, name = "receive_Question")

]
