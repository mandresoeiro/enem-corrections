from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class StudentProfile(models.Model):
    """Perfil de aluno."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile",
        help_text="Usuário ao qual este perfil pertence.",
    )

    bio = models.TextField(blank=True)

    course = models.CharField(
        max_length=200,
        blank=True,
        help_text="Curso do aluno (ex: Pré-ENEM, Redação Avançada).",
    )

    grade = models.CharField(max_length=20, blank=True)

    total_essays = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Perfil do aluno: {self.user.email}"


class TeacherProfile(models.Model):
    """Perfil de professor."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
        help_text="Usuário ao qual este perfil pertence.",
    )

    bio = models.TextField(blank=True)

    subjects = models.CharField(
        max_length=300, blank=True, help_text="Matérias ministradas pelo professor."
    )

    total_corrections = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Perfil do professor: {self.user.email}"
