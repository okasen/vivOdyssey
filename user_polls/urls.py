from django.urls import path
from .views import QAView

urlpatterns = [
    path('polls/', QAView.as_view(), name="polls"),
]
