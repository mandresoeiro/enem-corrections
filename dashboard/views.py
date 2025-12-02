from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from datetime import date, timedelta

from essays.models import Essay
from django.contrib.auth import get_user_model

from .services import dashboard_metrics
from .pdf import generate_pdf

User = get_user_model()


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """
    Dashboard principal que atende ALUNO, PROFESSOR e ADMIN.
    Agora com métricas completas, gráficos, listagens e KPIs.
    """

    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        role = getattr(user, "role", "guest")

        # 🔥 MÉTRICAS GERAIS DO USUÁRIO
        metrics = dashboard_metrics(user)

        ctx.update(
            {
                "role": role,
                "user": user,
                "title": metrics.get("title", "Dashboard"),
                "metrics": metrics,
            }
        )

        # 🔥 CARREGA DASHBOARD CORRETO
        if role == "student":
            ctx.update(self._context_student(user, metrics))

        elif role == "teacher":
            ctx.update(self._context_teacher(user, metrics))

        elif role == "admin":
            ctx.update(self._context_admin(user, metrics))

        return ctx

    # ======================================================================
    # 🟩 DASHBOARD DO ALUNO
    # ======================================================================
    def _context_student(self, user, metrics):
        essays = Essay.objects.filter(student=user).order_by("-created_at")

        last_essays = essays[:5]

        competencies = metrics.get("competencies", [0, 0, 0, 0, 0])

        return {
            "dashboard_template": "dashboard/student_dashboard.html",
            "avg_score": metrics.get("avg_score"),
            "essays_count": metrics.get("essays_count", 0),
            "pending_count": metrics.get("pending_count", 0),
            "best_competence": metrics.get("best_competence", "—"),
            "recent_essays": last_essays,
            "competencies": competencies,
        }

    # ======================================================================
    # 🟦 DASHBOARD DO PROFESSOR
    # ======================================================================
    def _context_teacher(self, user, metrics):
        # Correções dos últimos 7 dias
        labels = []
        values = []

        for i in range(6, -1, -1):
            day = date.today() - timedelta(days=i)
            labels.append(day.strftime("%d/%m"))

            values.append(
                Essay.objects.filter(status="corrected", updated_at__date=day).count()
            )

        return {
            "dashboard_template": "dashboard/teacher_dashboard.html",
            "today_count": metrics.get("today_count", 0),
            "total_corrected": metrics.get("total_corrected", 0),
            "pending_count": metrics.get("pending_count", 0),
            "avg_per_day": metrics.get("avg_per_day", 0),
            "labels": labels,
            "values": values,
            "pending": Essay.objects.filter(status="pending")[:10],
        }

    # ======================================================================
    # 🟥 DASHBOARD DO ADMINISTRADOR
    # ======================================================================
    def _context_admin(self, user, metrics):

        # Gráfico global: envios por dia (últimos 7 dias)
        labels = []
        values = []

        for i in range(6, -1, -1):
            day = date.today() - timedelta(days=i)
            labels.append(day.strftime("%d/%m"))
            values.append(Essay.objects.filter(created_at__date=day).count())

        return {
            "dashboard_template": "dashboard/admin_dashboard_pro.html",
            "users_count": metrics.get("users_count", 0),
            "teachers_count": metrics.get("teachers_count", 0),
            "essays_count": metrics.get("essays_count", 0),
            "pending_count": metrics.get("pending_count", 0),
            "labels": labels,
            "values": values,
            "recent_essays": Essay.objects.order_by("-created_at")[:10],
        }
