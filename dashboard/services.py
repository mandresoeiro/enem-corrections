from essays.models import Essay
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count

User = get_user_model()


def dashboard_metrics(user):
    """
    Métricas dinâmicas para Student, Teacher e Admin.
    Compatível com o modelo atual do usuário.
    """

    role = getattr(user, "role", "guest")

    # ======================
    # MÉTRICAS DO ALUNO
    # ======================
    if role == "student":
        essays = Essay.objects.filter(student=user)

        return {
            "title": "Dashboard do Aluno",
            "essays_count": essays.count(),
            "pending_count": essays.filter(status="pending").count(),
            "avg_score": essays.aggregate(Avg("score_total"))["score_total__avg"] or 0,
        }

    # ======================
    # MÉTRICAS DO PROFESSOR
    # ======================
    if role == "teacher":
        corrected = Essay.objects.filter(teacher=user, status="corrected")
        pending = Essay.objects.filter(teacher=user, status="pending")

        return {
            "title": "Painel do Professor",
            "total_corrected": corrected.count(),
            "pending_count": pending.count(),
        }

    # ======================
    # MÉTRICAS DO ADMIN
    # ======================
    if role == "admin":
        return {
            "title": "Administração Geral",
            "users_count": User.objects.count(),
            "teachers_count": User.objects.filter(role="teacher").count(),
            "essays_count": Essay.objects.count(),
            "pending_count": Essay.objects.filter(status="pending").count(),
        }

    return {"title": "Dashboard"}
