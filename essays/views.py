"""
Views do módulo de redações ENEM.

Responsabilidades:
- Permitir que o aluno envie redações.
- Permitir listagem das próprias redações.
- Permitir ao professor corrigir uma redação (CompetenceScore).
- Implementar regras de permissão baseadas em roles:
    - student → pode criar e listar suas redações
    - teacher → pode corrigir redações
    - admin → pode fazer tudo
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from performance.services.performance_service import PerformanceService


from .models import Essay, CompetenceScore
from .serializers import EssaySerializer, CompetenceScoreSerializer


# ==========================================================
# 1. Permissões baseadas no papel do usuário
# ==========================================================


class IsStudent(permissions.BasePermission):
    """Permite acesso apenas para usuários com role = student."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"


class IsTeacher(permissions.BasePermission):
    """Permite acesso apenas para usuários com role = teacher."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "teacher"


# ==========================================================
# 2. CREATE — Aluno envia redação
# ==========================================================


class EssayCreateView(generics.CreateAPIView):
    """
    Permite que o aluno envie uma nova redação.

    Regra:
    - Apenas student pode criar.
    - student é atribuído automaticamente.
    """

    serializer_class = EssaySerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        # Define automaticamente o aluno dono da redação
        serializer.save(student=self.request.user)


# ==========================================================
# 3. LIST — Aluno visualiza suas próprias redações
# ==========================================================


class EssayListView(generics.ListAPIView):
    """
    Lista todas as redações enviadas pelo aluno logado.

    Regra:
    - Student vê apenas suas redações.
    - Teacher e Admin poderiam ver todas se quiséssemos,
      mas aqui mantemos restrito ao aluno.
    """

    serializer_class = EssaySerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Essay.objects.filter(student=self.request.user).order_by("-created_at")


# ==========================================================
# 4. CORREÇÃO — Professor corrige redação enviada por um aluno
# ==========================================================


class EssayCorrectionView(generics.CreateAPIView):
    """
    Professores corrigem redações enviando notas ENEM para c1...c5.

    Fluxo completo:
    - Professor envia POST /api/essays/<id>/correct/
    - O backend:
        1. cria CompetenceScore
        2. marca a redação como CORRIGIDA
        3. calcula score_total = soma das 5 competências
        4. registra quem corrigiu
    """

    serializer_class = CompetenceScoreSerializer
    permission_classes = [IsTeacher]

    def perform_create(self, serializer):
        # ID da redação vem pela URL
        essay_id = self.kwargs["essay_id"]
        essay = get_object_or_404(Essay, id=essay_id)

        # Atualiza status e nota total
        c1 = serializer.validated_data["c1"]
        c2 = serializer.validated_data["c2"]
        c3 = serializer.validated_data["c3"]
        c4 = serializer.validated_data["c4"]
        c5 = serializer.validated_data["c5"]

        total = c1 + c2 + c3 + c4 + c5

        essay.status = Essay.Status.CORRECTED
        essay.score_total = total
        essay.save()

        # Cria o objeto de competências
        serializer.save(
            essay=essay,
            corrected_by=self.request.user,
        )
