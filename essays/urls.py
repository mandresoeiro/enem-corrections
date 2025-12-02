"""
Rotas do módulo de Redações ENEM.

Cada rota usa uma view responsável:
- EssayCreateView → aluno envia redação
- EssayListView → aluno vê suas redações
- EssayCorrectionView → professor corrige redação por ID
"""

from django.urls import path
from .views import (
    EssayCreateView,
    EssayListView,
    EssayCorrectionView,
)

app_name = "essays"

urlpatterns = [
    # ==========================================================
    # 1. Aluno envia uma nova redação
    # POST /api/essays/create/
    # ==========================================================
    path("create/", EssayCreateView.as_view(), name="essay-create"),
    # ==========================================================
    # 2. Aluno lista suas próprias redações
    # GET /api/essays/my/
    # ==========================================================
    path("my/", EssayListView.as_view(), name="essay-list"),
    # ==========================================================
    # 3. Professor corrige uma redação por ID
    # POST /api/essays/<ID>/correct/
    # ==========================================================
    path(
        "<int:essay_id>/correct/", EssayCorrectionView.as_view(), name="essay-correct"
    ),
]
