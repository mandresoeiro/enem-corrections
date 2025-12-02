from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Modelo de usuário customizado baseado em AbstractUser.

    Mantém toda a estrutura padrão do Django (username, senha, etc.),
    mas adiciona:
    - login por email (como identificador principal)
    - campo de `role` para diferenciar aluno, professor e admin.
    """

    class Role(models.TextChoices):
        """Enum interno com papéis disponíveis no sistema."""

        STUDENT = "student", "Student"
        TEACHER = "teacher", "Teacher"
        ADMIN = "admin", "Admin"

    # Email único → importante para autenticação e comunicação.
    email = models.EmailField(
        "email address",
        unique=True,
        help_text="Email único usado para login e comunicação.",
    )

    # Papel principal do usuário na plataforma
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text="Papel principal do usuário no sistema (student/teacher/admin).",
    )

    # Campos de auditoria (boas práticas)
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Data/hora de criação do usuário.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Data/hora da última atualização do usuário.",
    )

    # Login será feito por email (profissional)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # ainda pedimos username ao criar superuser

    def __str__(self) -> str:
        """Retorna representação elegante do usuário."""
        display = self.get_full_name() or self.username or self.email
        return f"{display} ({self.role})"

    # -----------------
    # Helpers de papel
    # -----------------

    @property
    def is_student(self) -> bool:
        """Retorna True se o usuário for aluno."""
        return self.role == self.Role.STUDENT

    @property
    def is_teacher(self) -> bool:
        """Retorna True se o usuário for professor."""
        return self.role == self.Role.TEACHER

    @property
    def is_admin(self) -> bool:
        """Retorna True se o usuário for admin de negócio (não confundir com superuser)."""
        return self.role == self.Role.ADMIN


# TODO
"""💡 Dica: manter username ainda é útil pro admin, logs e integração com allauth.
A gente só troca o identificador principal para email."""
