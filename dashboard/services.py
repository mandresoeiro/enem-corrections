from django.db.models import Avg
from django.contrib.auth import get_user_model
from datetime import date, timedelta

from essays.models import Essay

User = get_user_model()


def dashboard_metrics(user):
    """
    Retorna métricas específicas para o papel do usuário.

    Encaminha para a função especializada conforme o role.
    Garante separação de responsabilidades e modularidade.

    Args:
        user (User): instância do usuário autenticado

    Returns:
        dict: dicionário com métricas para o dashboard
    """
    if not hasattr(user, "role"):
        raise ValueError("Usuário sem 'role' definido.")

    match user.role:
        case "student":
            return _metrics_student(user)
        case "teacher":
            return _metrics_teacher(user)
        case "admin":
            return _metrics_admin(user)
        case _:
            return {"title": "Dashboard"}


def _metrics_student(user):
    essays = Essay.objects.filter(student=user)
    return {
        "title": "Dashboard do Aluno",
        "essays_count": essays.count(),
        "pending_count": essays.filter(status="pending").count(),
        "avg_score": essays.aggregate(Avg("score_total"))["score_total__avg"] or 0,
    }


def _metrics_teacher(user):
    from essays.models import CompetenceScore, Essay

    corrected = CompetenceScore.objects.filter(corrected_by=user).count()
    pending = Essay.objects.filter(status="pending").count()
    return {
        "title": "Painel do Professor",
        "total_corrected": corrected,
        "pending_count": pending,
    }


def _metrics_admin(user):
    return {
        "title": "Administração Geral",
        "users_count": User.objects.count(),
        "teachers_count": User.objects.filter(role="teacher").count(),
        "essays_count": Essay.objects.count(),
        "pending_count": Essay.objects.filter(status="pending").count(),
    }


def get_dashboard_context(user, role, metrics):
    """
    Retorna o contexto adicional para renderizar o dashboard correto
    baseado no papel do usuário.

    Args:
        user (User): instância autenticada
        role (str): papel do usuário ("student", "teacher", "admin")
        metrics (dict): dicionário de métricas base

    Returns:
        dict: contexto estendido com dados específicos
    """
    if role == "student":
        return _context_student(user, metrics)
    elif role == "teacher":
        return _context_teacher(user, metrics)
    elif role == "admin":
        return _context_admin(user, metrics)
    return {}


def _context_student(user, metrics):
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


def _context_teacher(user, metrics):
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


def _context_admin(user, metrics):
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
