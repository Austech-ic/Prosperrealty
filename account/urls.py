from django.urls import path
from .views import *

urlpatterns = [
    path("auth/login/",LoginUserAPiView.as_view()),
    path("auth/register/",UserRegistrationApiView.as_view()),
    path("auth/user/profile/",UserProfileApiView.as_view())
]