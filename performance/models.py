# Performance model placeholder
from django.db import models
from django.conf import settings
from essays.models import Essay, CompetenceScore

User = settings.AUTH_USER_MODEL


# ==========================================================
# 1. Performance geral do aluno (dados agregados)
# ==========================================================
class StudentPerformance(models.Model):
    """
    Tabela que armazena indicadores gerais de desempenho do aluno.

    Objetivos:
    - Reduzir consultas pesadas repetidas.
    - Servir como base para dashboards e gráficos rápidos.
    - Atualizada automaticamente sempre que uma redação é corrigida.
    """

    student = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="performance",
        help_text="Aluno ao qual esta performance pertence.",
    )

    # Média geral ENEM do aluno
    average_score = models.FloatField(default=0)

    # Total de redações corrigidas
    total_essays_corrected = models.PositiveIntegerField(default=0)

    # Média por competência
    avg_c1 = models.FloatField(default=0)
    avg_c2 = models.FloatField(default=0)
    avg_c3 = models.FloatField(default=0)
    avg_c4 = models.FloatField(default=0)
    avg_c5 = models.FloatField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Performance de {self.student.email}"


# ==========================================================
# 2. Histórico de competências por redação (evolução ponto-a-ponto)
# ==========================================================
class CompetenceHistory(models.Model):
    """
    Cada linha registra a nota das competências ENEM de UMA redação.
    Usado para gerar gráficos de linha, radar e evolução.

    - Permite traçar a curva de aprendizado do aluno.
    - Permite ao professor identificar padrões de dificuldade.
    """

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="competence_history",
    )

    essay = models.ForeignKey(
        Essay,
        on_delete=models.CASCADE,
        related_name="competence_history",
    )

    # Notas das competências
    c1 = models.PositiveIntegerField(default=0)
    c2 = models.PositiveIntegerField(default=0)
    c3 = models.PositiveIntegerField(default=0)
    c4 = models.PositiveIntegerField(default=0)
    c5 = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        return self.c1 + self.c2 + self.c3 + self.c4 + self.c5

    def __str__(self):
        return f"Histórico ENEM de {self.student.email} — redação {self.essay.id}"


# ==========================================================
# 3. Evolução mensal agregada (dashboard temporal)
# ==========================================================
class MonthlyEvolution(models.Model):
    """
    Armazena a média mensal do aluno para gráficos de barras/linhas.

    Exemplo:
    - mês 5 de 2025 → média geral 720
    - mês 6 de 2025 → média geral 760 → mostra evolução

    Permite análises temporais e insights sobre progresso.
    """

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="monthly_evolution",
    )

    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()

    avg_score_month = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "year", "month")

    def __str__(self):
        return f"Evolução mensal: {self.student.email} {self.month}/{self.year}"
