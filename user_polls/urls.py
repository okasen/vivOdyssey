from django.urls import path

from .views import QAView, receiveQuestion

urlpatterns = [
    path('polls/', QAView.as_view(), name="polls"),
    path('get/ajax/validate/question/', receiveQuestion, name = "receive_Question")

]
