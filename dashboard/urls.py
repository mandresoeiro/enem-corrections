app_name = "dashboard"
from django.urls import path
from .views import DashboardHomeView, EssayPDFUploadView, EssayPDFFlipbookView

urlpatterns = [
    path("", DashboardHomeView.as_view(), name="dashboard"),
    path("<str:role>/", DashboardHomeView.as_view(), name="dashboard-role"),
    path("pdf/", EssayPDFUploadView.as_view(), name="pdf-upload"),
    path("pdf/flipbook/<int:essay_id>/", EssayPDFFlipbookView.as_view(), name="pdf-flipbook"),
]
