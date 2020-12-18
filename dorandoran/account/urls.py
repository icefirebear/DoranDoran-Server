from django.urls import path
from .views import (
    RegistrationView,
    LoginView,
    SignOutView,
    RefreshJSONWebTokenView,
    UserInfoView,
)

urlpatterns = [
    path("sign-up", RegistrationView.as_view()),
    path("login", LoginView.as_view()),
    path("sign-out", SignOutView.as_view()),
    path("refresh", RefreshJSONWebTokenView.as_view()),
    path("my-info", UserInfoView.as_view()),
]
