"""
Serializers do módulo de Redações ENEM.

Responsabilidades:
- Converter modelos Essay e CompetenceScore para JSON.
- Garantir segurança e controle de quem altera o quê.
- Regras de negócio essenciais ficam nas views, mas proteções básicas ficam aqui.

Padrões aplicados:
- Segurança: campos controlados pelo backend são read-only.
- Limpeza: serializer enxuto, porém documentado.
- Pronto para integrações com React + Vite.
"""

from rest_framework import serializers
from .models import Essay, CompetenceScore


# ==========================================================
# 1. EssaySerializer
# ==========================================================
class EssaySerializer(serializers.ModelSerializer):
    """
    Serializador principal da redação enviada pelo aluno.

    Observações do Tech Lead:
    - O aluno NÃO escolhe 'student'. Isso é definido via request.user.
    - 'status' e 'score_total' são controlados apenas pelo backend.
    - Nunca exponha campos controlados pelo servidor para escrita.
    """

    class Meta:
        model = Essay
        fields = [
            "id",
            "student",  # somente leitura
            "title",
            "text",
            "status",  # somente leitura
            "score_total",  # somente leitura
            "created_at",
            "updated_at",
        ]

        # Segurança: impede que o cliente force valores indevidos
        read_only_fields = [
            "student",
            "status",
            "score_total",
            "created_at",
            "updated_at",
        ]


# ==========================================================
# 2. CompetenceScoreSerializer
# ==========================================================
class CompetenceScoreSerializer(serializers.ModelSerializer):
    """
    Serializador das notas ENEM (c1...c5) atribuídas pelo professor.

    Considerações:
    - corrected_by é preenchido automaticamente na view.
    - corrected_at também é automático.
    - O professor NÃO escolhe a redação — vem pela URL.
    """

    class Meta:
        model = CompetenceScore
        fields = [
            "c1",
            "c2",
            "c3",
            "c4",
            "c5",
            "corrected_by",  # leitura
            "corrected_at",  # leitura
        ]

        read_only_fields = [
            "corrected_by",
            "corrected_at",
        ]
