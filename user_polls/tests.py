from django.test import TestCase
from .models import Question, Answer
from accounts.models import Player
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import Permission

# Create your tests here.

class QuestionModelTest(TestCase):
    def setUp(self):
        Question.objects.create(title="title test", text="text test")

    def test_text_label(self):
        question = Question.objects.get(title="title test")
        field_label = question._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'short description of the question')


class AnswerModelTest(TestCase):
    def setUp(self):
        q = Question.objects.create(title="title test", text="text test")
        u = Player.objects.create(email='nonyemail@noemail.net', username="answername", password="p4ssW3rd1234")
        q.save()
        Answer.objects.create(user=u, question=q, answer="answer test", date_answered = timezone.now())
    
    def test_answer_label(self):
        answer = Answer.objects.get(id=1)
        field_label = answer._meta.get_field('answer').verbose_name
        self.assertEqual(field_label, 'Give your input')

class QandAnswerViewsTest(TestCase):
    number_of_questions = 50
    
    @classmethod
    def setUpTestData(cls):
        answers_per_question = 3
        u = Player.objects.create(email='nopeyymail@noemail.net', username="testername", password="p4ssW3rd1234")
        u.save()

        for qid in range(50):
            Question.objects.create(title={qid}, text={qid})
            for aid in range(answers_per_question):
                q = Question.objects.get(title={qid})
                Answer.objects.create(user=u, question=q, answer={aid}, date_answered = timezone.now())

        qid = 0
    #for the view all questions view. These tests currently seem broken syntax-
    def test_base_url_exists_at_correct_location(self):
        response = self.client.get('/polls/answer/all/')
        self.assertEqual(response.status_code, 200)
            
    def test_lists_questions_exists(self):
        response = self.client.get('/polls/answer/all/')
        self.assertEqual(response.status_code, 200)

##    def test_redirect_unlogged_users(self): #not yet implemented, should fail currently
##        response = self.client.get(reverse('all'))
##        self.assertRedirects(response, '/accounts/login/')
##
##    def test_logged_in_can_view(self): #not yet implemented, should false positive currently
##        login = self.client.login(username='testername', password='p4ssW3rd1234')
##        response = self.client.get(reverse('all'))

        #check user is logged in (that user is testername)
##        user = response.wsgi_request.user.get()
##        self.assertEqual(str(response.context['user']), 'testername')
##        #check that they were successful
##        self.assertEqual(response.status_code, 200)
        
    def test_view_accessible_by_name(self):
        response = self.client.get('/polls/answer/5/')
        self.assertEqual(response.status_code, 200)

    def test_view_template_correct(self):
        response = self.client.get('/polls/answer/5/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_polls/polls/answer.html')
        
        
    #for the answers given view
    def test_answers_url_exists_at_correct_location(self):
        response = self.client.get('/polls/answer/5/answers/')
        self.assertEqual(response.status_code, 200)

    def test_answers_view_accessible_by_name(self):
        response = self.client.get('/polls/answer/5/answers/')
        self.assertEqual(response.status_code, 200)

    def test_answers_view_template_correct(self):
        response = self.client.get('/polls/answer/5/answers/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_polls/polls/answers_given.html')
        
##class QAViewTest(TestCase):
##    authorized = Player.objects.create(email='noyyeemail@noemail.net', username="authorised", password="p4ssW3rd1234")
##    authorized.save()
##    unauthorized = Player.objects.create(email='nonyeemail@noemail.net', username="unauth", password="p4ssW3rd1234")
##    unauthorized.save()

    #permission = Permission.objects.get(name='can_add_question')
    #authorized.user_permissions.add(permission)

##    def QAV_test_redirect_unlogged_users(self): #not yet implemented, should fail currently
##        response = self.client.get(reverse('moderation'))
##        self.assertRedirects(response, '/accounts/login/')

##    def QAV_test_logged_in_cannot_view_without_permission(self): #not yet implemented, should fail currently
##        login = self.client.login(username='unauth', password='p4ssW3rd1234')
##        response = self.client.get(reverse('moderation'))
##
##        #check user is logged in (that user is testername)
##        self.assertEqual(str(response.context_data['user']), 'unauth')
##        #check that they were not successful
##        self.assertEqual(response.status_code, 403) #status code is forbidden
##
##    def QAV_test_logged_in_can_view_with_permission(self): #not yet implemented, should false positive currently
##        login = self.client.login(username='authorised', password='p4ssW3rd1234')
##        response = self.client.get(reverse('moderation'))
##
##        #check user is logged in (that user is testername)
##        self.assertEqual(str(response.context_data['user']), 'authorised')
##        #check that they were successful
##        self.assertEqual(response.status_code, 200) #status code is forbidden
