from django.urls import path
from .views import (
    RecruiterSignupView, SeekerSignupView, LoginView,
    LogoutView, RecruiterProfileView, SeekerProfileView
)

urlpatterns = [
    path('recruiter/signup/', RecruiterSignupView.as_view()),
    path('seeker/signup/', SeekerSignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('recruiterprofile/', RecruiterProfileView.as_view()),
    path('seekerprofile/', SeekerProfileView.as_view()),
]
