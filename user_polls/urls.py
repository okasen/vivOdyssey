from django.urls import path

from .views import QAView, receiveQuestion

urlpatterns = [
    path('polls/', QAView.as_view(), name="polls"),
    path('post/ajax/question',  QAView.postQuestion, name = "post_question"),
    path('get/ajax/validate/nickname', receiveQuestion, name = "receive_Question")

]
