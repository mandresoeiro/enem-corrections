from django.urls import path
from .views import (
    DashboardStudentMetrics,
    DashboardTeacherMetrics,
    DashboardAdminMetrics,
    DashboardMe,
)

app_name = "performance"

urlpatterns = [
    # Endpoint universal
    path("me/", DashboardMe.as_view(), name="dashboard-me"),
    # Endpoints individuais
    path("student/", DashboardStudentMetrics.as_view(), name="dashboard-student"),
    path("teacher/", DashboardTeacherMetrics.as_view(), name="dashboard-teacher"),
    path("admin/", DashboardAdminMetrics.as_view(), name="dashboard-admin"),
]
