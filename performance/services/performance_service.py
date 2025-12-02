"""
Service Layer responsável por atualizar as métricas de performance do aluno.

Chamado automaticamente quando o professor corrige uma redação.
"""

from datetime import datetime
from django.db.models import Avg
from performance.models import (
    StudentPerformance,
    CompetenceHistory,
    MonthlyEvolution,
)
from essays.models import Essay, CompetenceScore


class PerformanceService:
    """
    Camada de serviço para atualizar métricas de forma limpa e escalável.

    Chamado em EssayCorrectionView → perform_create()
    """

    @staticmethod
    def update_all_metrics(essay: Essay, competence: CompetenceScore):
        """
        Atualiza:
        - histórico ponto-a-ponto
        - métricas agregadas
        - evolução mensal
        """

        PerformanceService._save_competence_history(essay, competence)
        PerformanceService._update_student_performance(essay.student)
        PerformanceService._update_monthly_evolution(essay, competence)

    # ==========================================================
    # 1. Histórico da redação (ponto no gráfico)
    # ==========================================================
    @staticmethod
    def _save_competence_history(essay: Essay, competence: CompetenceScore):
        CompetenceHistory.objects.create(
            student=essay.student,
            essay=essay,
            c1=competence.c1,
            c2=competence.c2,
            c3=competence.c3,
            c4=competence.c4,
            c5=competence.c5,
        )

    # ==========================================================
    # 2. Atualiza agregações gerais
    # ==========================================================
    @staticmethod
    def _update_student_performance(student):
        """
        Atualiza automaticamente:
        - média geral
        - média por competência
        - total de redações corrigidas
        """

        corrections = CompetenceScore.objects.filter(essay__student=student)

        if not corrections.exists():
            return

        perf, _ = StudentPerformance.objects.get_or_create(student=student)

        perf.total_essays_corrected = corrections.count()

        perf.average_score = (
            corrections.aggregate(
                total=Avg(
                    (
                        models.F("c1")
                        + models.F("c2")
                        + models.F("c3")
                        + models.F("c4")
                        + models.F("c5")
                    )
                )
            )["total"]
            or 0
        )

        perf.avg_c1 = corrections.aggregate(Avg("c1"))["c1__avg"] or 0
        perf.avg_c2 = corrections.aggregate(Avg("c2"))["c2__avg"] or 0
        perf.avg_c3 = corrections.aggregate(Avg("c3"))["c3__avg"] or 0
        perf.avg_c4 = corrections.aggregate(Avg("c4"))["c4__avg"] or 0
        perf.avg_c5 = corrections.aggregate(Avg("c5"))["c5__avg"] or 0

        perf.save()

    # ==========================================================
    # 3. Atualiza evolução mensal
    # ==========================================================
    @staticmethod
    def _update_monthly_evolution(essay: Essay, competence: CompetenceScore):
        """
        Registra a média do mês corrente.
        O gráfico de evolução usa esses dados.
        """

        now = datetime.now()
        month = now.month
        year = now.year

        total = (
            competence.c1
            + competence.c2
            + competence.c3
            + competence.c4
            + competence.c5
        )

        evolution, created = MonthlyEvolution.objects.get_or_create(
            student=essay.student,
            month=month,
            year=year,
            defaults={"avg_score_month": total},
        )

        if not created:
            # atualizar média mensal recalculando baseado no histórico
            all_scores = CompetenceHistory.objects.filter(
                student=essay.student, created_at__year=year, created_at__month=month
            )

            new_avg = (
                all_scores.aggregate(
                    avg=Avg(
                        (
                            models.F("c1")
                            + models.F("c2")
                            + models.F("c3")
                            + models.F("c4")
                            + models.F("c5")
                        )
                    )
                )["avg"]
                or total
            )

            evolution.avg_score_month = new_avg
            evolution.save()
