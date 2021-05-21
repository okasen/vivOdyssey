from django.urls import path
from .views import ViewOwnProfile, ViewOtherProfile

urlpatterns = [
    path('you/', ViewOwnProfile.as_view(), name="own-profile"),
    path('<int:user_id>/', ViewOtherProfile.as_view(), name="other-profile"),
    ]
