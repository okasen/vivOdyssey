from .models import Question, Answer
from django import forms
from django.utils import timezone

class QuestionCreate(forms.ModelForm): #should only be accessible by admin or moderator
    def __init__(self, *args, **kwargs):
        super(QuestionCreate, self).__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ("__all__")
            
class AnswerForm(forms.ModelForm): #accessible by anyone logged in
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ("__all__")

        exclude = ['date_answered', 'user', 'question']
