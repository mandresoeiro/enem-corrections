from django.urls import path
from django.views.generic import TemplateView
from .views import MeView

app_name = "accounts"

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    # Rotas HTML (login/register/forgot)
    path(
        "login/",
        TemplateView.as_view(template_name="accounts/login.html"),
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
]
