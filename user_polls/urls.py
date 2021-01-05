from django.urls import path

from .views import QAView

urlpatterns = [
    path('polls/', QAView.questionView, name='polls'),
    path('post/ajax/question',  QAView.postQuestion, name = "post_question"),
    path('get/ajax/validate/nickname', QAView.receiveQuestion, name = "receive_Question")

]
