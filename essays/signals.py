from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CompetenceScore


@receiver(post_save, sender=CompetenceScore)
def update_essay_score(sender, instance, **kwargs):
    """
    Sempre que as competências forem criadas/alteradas,
    a nota total da redação é atualizada automaticamente.
    """
    instance.essay.update_total()
