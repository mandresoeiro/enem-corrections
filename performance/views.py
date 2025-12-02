from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from essays.models import Essay, CompetenceScore
from accounts.models import CustomUser
from django.db.models import Avg


class IsStudentOrTeacher(permissions.BasePermission):
    """
    Permite acesso a qualquer usuário autenticado.
    Futuramente podemos separar permissões por role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated


# ==========================================================
# 1) API DO ALUNO /api/performance/student/
# ==========================================================


class DashboardStudentMetrics(APIView):
    """
    Retorna métricas para o aluno:
    - total de redações enviadas
    - última nota corrigida
    - média geral das competências ENEM
    """

    permission_classes = [IsStudentOrTeacher]

    def get(self, request):
        user = request.user

        # Total de redações enviadas pelo aluno
        total_essays = Essay.objects.filter(student=user).count()

        # Última redação corrigida
        last_corrected = (
            Essay.objects.filter(student=user, status="corrected")
            .order_by("-updated_at")
            .first()
        )
        last_score = last_corrected.score_total if last_corrected else None

        # Média das 5 competências ENEM
        avg = CompetenceScore.objects.filter(essay__student=user).aggregate(
            avg_c1=Avg("c1"),
            avg_c2=Avg("c2"),
            avg_c3=Avg("c3"),
            avg_c4=Avg("c4"),
            avg_c5=Avg("c5"),
        )

        if avg["avg_c1"]:
            average_score = (
                avg["avg_c1"]
                + avg["avg_c2"]
                + avg["avg_c3"]
                + avg["avg_c4"]
                + avg["avg_c5"]
            )
        else:
            average_score = None

        return Response(
            {
                "essays_total": total_essays,
                "last_score": last_score,
                "average_score": average_score,
            }
        )


# ==========================================================
# 2) API DO PROFESSOR /api/performance/teacher/
# ==========================================================


class DashboardTeacherMetrics(APIView):
    """
    Métricas do professor:
    - redações pendentes para correção
    - correções realizadas por ele
    """

    permission_classes = [IsStudentOrTeacher]

    def get(self, request):
        user = request.user

        pending = Essay.objects.filter(status="submitted").count()
        corrected = CompetenceScore.objects.filter(corrected_by=user).count()

        return Response(
            {
                "pending_essays": pending,
                "corrections_done": corrected,
            }
        )


# ==========================================================
# 3) API ADMIN /api/performance/admin/
# ==========================================================


class DashboardAdminMetrics(APIView):
    """
    Métricas gerais para administradores do sistema.
    """

    permission_classes = [IsStudentOrTeacher]

    def get(self, request):

        users_total = CustomUser.objects.count()
        students_total = CustomUser.objects.filter(role="student").count()
        teachers_total = CustomUser.objects.filter(role="teacher").count()
        essays_total = Essay.objects.count()

        return Response(
            {
                "users_total": users_total,
                "students_total": students_total,
                "teachers_total": teachers_total,
                "essays_total": essays_total,
            }
        )


# ==========================================================
# 4) /me/ — Retorna automaticamente o dashboard correto
# ==========================================================


class DashboardMe(APIView):
    """
    Endpoint unificado.
    Dependendo do papel do usuário (role),
    retorna os dados do dashboard correspondente.
    """

    permission_classes = [IsStudentOrTeacher]

    def get(self, request):

        role = request.user.role

        if role == "student":
            return DashboardStudentMetrics().get(request)

        if role == "teacher":
            return DashboardTeacherMetrics().get(request)

        if role == "admin":
            return DashboardAdminMetrics().get(request)

        return Response({"detail": "Role desconhecida"}, status=400)
