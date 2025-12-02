from django.urls import path
from .views import ProfileHomeView

app_name = "profiles"

urlpatterns = [
    path("", ProfileHomeView.as_view(), name="profile-home"),
]
