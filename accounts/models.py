from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Modelo de usuário customizado baseado em AbstractUser.

    Melhorias aplicadas:
    - Email como identificador principal (USERNAME_FIELD)
    - Papel do usuário (student/teacher/admin)
    - Campos de auditoria
    - Métodos auxiliares para checar papel
    """

    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        TEACHER = "teacher", "Teacher"
        ADMIN = "admin", "Admin"

    # Email único como campo obrigatório
    email = models.EmailField(
        "email address",
        unique=True,
        db_index=True,
        help_text="Email único usado como identificador principal de login.",
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text="Papel principal do usuário no sistema.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Data/hora de criação do usuário.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Data/hora da última atualização do usuário.",
    )

    # Login por email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        display = self.get_full_name() or self.username or self.email
        return f"{display} ({self.role})"

    # Helpers de papel
    @property
    def is_student(self) -> bool:
        return self.role == self.Role.STUDENT

    @property
    def is_teacher(self) -> bool:
        return self.role == self.Role.TEACHER

    @property
    def is_admin(self) -> bool:
        return self.role == self.Role.ADMIN
