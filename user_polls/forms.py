from .models import Question, Answer
from django import forms
import datetime

class QuestionCreate(forms.ModelForm): #should only be accessible by admin
    def __init__(self, *args, **kwargs):
        super(QuestionCreate, self).__init__(*args, **kwargs)

        for name in self.field.keys():
            self.field[name].widget.attrs.update({
                'class': 'form-control',
            })

        class Meta:
            model = Question
            fields = ("__all__")
            
class AnswerForm(forms.ModelForm): #accessible by anyone logged in
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

        for name in self.field.keys():
            self.field[name].widget.attrs.update({
                'class': 'form-control',
            })

        class Meta:
            model = Answer
            fields = ("__all__")
