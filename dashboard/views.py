
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from .pdf import generate_pdf
from django.contrib.auth import get_user_model
from essays.models import Essay

from .services import dashboard_metrics, get_dashboard_context

User = get_user_model()

class EssayPDFFlipbookView(LoginRequiredMixin, View):
    def get(self, request, essay_id, *args, **kwargs):
        # Monta a URL do PDF
        # Buscar o Essay e usar o campo pdf, se disponível
        try:
            essay = Essay.objects.get(id=essay_id)
            if essay.pdf:
                pdf_url = essay.pdf.url
            else:
                pdf_url = f"/media/pdfs/{essay_id}.pdf"
        except Essay.DoesNotExist:
            pdf_url = None
        return render(request, "dashboard/pdf_flipbook.html", {"pdf_url": pdf_url})


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """
    Dashboard principal que atende ALUNO, PROFESSOR e ADMIN.
    Agora com métricas completas, gráficos, listagens e KPIs.
    """

    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        if not hasattr(user, "role"):
            raise ValueError("Usuário sem role definido.")

        role = user.role

        # 🔥 MÉTRICAS GERAIS DO USUÁRIO
        metrics = dashboard_metrics(user)

        ctx.update(
            {
                "role": role,
                "user": user,
                "title": metrics.get("title", "Dashboard"),
                "metrics": metrics,
            }
        )

        # 🔥 CONTEXTO DO DASHBOARD POR PAPEL
        ctx.update(get_dashboard_context(user, role, metrics))

        # ✅ Dados adicionais para os templates, evitando lógicas diretas no HTML
        if role == "teacher":
            from essays.models import CompetenceScore

            ctx["corrected_essays_count"] = CompetenceScore.objects.filter(
                corrected_by=user
            ).count()
            ctx["pending_essays_count"] = Essay.objects.filter(status="pending").count()
            ctx["show_teacher_cards"] = True

            # Listar redações enviadas (exemplo: status=submitted ou corrected)
            essays = Essay.objects.filter(status__in=[Essay.Status.SUBMITTED, Essay.Status.CORRECTED]).select_related('student').order_by('-created_at')[:20]
            # Adicionar campo pdf_url: prioriza o upload, senão usa caminho antigo
            for essay in essays:
                if essay.pdf:
                    essay.pdf_url = essay.pdf.url
                else:
                    essay.pdf_url = f"/media/pdfs/{essay.id}.pdf"
            ctx["essays"] = essays

        elif role == "student":
            ctx["corrected_essays_count"] = Essay.objects.filter(
                student=user, status="corrected"
            ).count()
            ctx["pending_essays_count"] = Essay.objects.filter(
                student=user, status="pending"
            ).count()
            ctx["show_student_cards"] = True

        elif role == "admin":
            ctx["corrected_essays_count"] = Essay.objects.filter(
                status="corrected"
            ).count()
            ctx["pending_essays_count"] = Essay.objects.filter(status="pending").count()
            ctx["total_users"] = User.objects.count()
            ctx["show_admin_cards"] = True

        return ctx


# View profissional para upload/envio automático de PDF
class EssayPDFUploadView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        texto = request.POST.get('texto')
        titulo = request.POST.get('titulo')
        user = request.user
        pdf_file = request.FILES.get('pdf')

        essay_obj = Essay(
            student=user,
            title=titulo,
            text=texto,
            status=Essay.Status.SUBMITTED
        )
        if pdf_file:
            essay_obj.pdf = pdf_file
        essay_obj.save()

        # Gere o PDF automaticamente se não foi enviado
        if not pdf_file:
            essay_data = {'titulo': titulo, 'texto': texto}
            pdf_path = generate_pdf(essay_data, essay_id=essay_obj.id)
            # Opcional: salvar o PDF gerado no campo pdf
            # with open(pdf_path, 'rb') as f:
            #     essay_obj.pdf.save(f"{essay_obj.id}.pdf", f, save=True)

        return redirect('dashboard:dashboard-role', role='teacher')

    def get(self, request, *args, **kwargs):
        # Exibe formulário simples para upload (pode ser removido se for 100% automático)
        return render(request, 'dashboard/pdf_upload.html')
