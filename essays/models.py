from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

User = settings.AUTH_USER_MODEL


class Essay(models.Model):
    pdf = models.FileField(upload_to="pdfs/", null=True, blank=True, help_text="Arquivo PDF da redação (upload manual ou automático)")
    """
    Redação enviada por um aluno.
    Agora funciona como a entidade "Agregadora".
    """

    class Status(models.TextChoices):
        DRAFT = "draft", "Rascunho"
        SUBMITTED = "submitted", "Enviada"
        CORRECTED = "corrected", "Corrigida"

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="essays",
    )

    title = models.CharField(max_length=255)
    text = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    score_total = models.PositiveIntegerField(
        null=True, blank=True, help_text="Nota final ENEM (0–1000)."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total(self):
        """
        Soma das 5 competências — usado pelo signal.
        """
        if hasattr(self, "competence_score"):
            self.score_total = self.competence_score.total()
            self.status = Essay.Status.CORRECTED
            self.save(update_fields=["score_total", "status"])

    def __str__(self):
        return f"Redação {self.title} ({self.student.email})"


class CompetenceScore(models.Model):
    """
    Notas das competências ENEM.
    """

    essay = models.OneToOneField(
        Essay,
        on_delete=models.CASCADE,
        related_name="competence_score",
    )

    c1 = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    c2 = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    c3 = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    c4 = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    c5 = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(200)]
    )

    corrected_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="corrections_done",
    )

    corrected_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        """ENEM = soma das 5 competências (0–1000)."""
        return self.c1 + self.c2 + self.c3 + self.c4 + self.c5

    def __str__(self):
        return f"Notas da redação {self.essay.id}"
