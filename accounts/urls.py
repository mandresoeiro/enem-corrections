from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import MeView

app_name = "accounts"

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    # Rotas HTML (login/register/forgot)
    path(
        "login/",
        LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "register/",
        TemplateView.as_view(template_name="accounts/register.html"),
        name="register",
    ),
    path(
        "forgot-password/",
        TemplateView.as_view(template_name="accounts/forgot_password.html"),
        name="forgot-password",
    ),
    path("logout/", LogoutView.as_view(next_page="/accounts/login/"), name="logout"),
]
