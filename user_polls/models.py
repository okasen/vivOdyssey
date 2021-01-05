from django.db import models
from accounts.models import Player

# Create your models here.

#I need to be able to add questions
#users need to be able to answer them
#users need to be able to see and maybe edit answers
#I need to be able to see the answers

class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField('short description of the question', max_length=280)

class Answer(models.Model):
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField('Give your input')
    date_answered = models.DateTimeField('User answered at this time')
    
