import requests
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View

from essays.models import Essay

from .pdf import generate_pdf
from .services import dashboard_metrics, get_dashboard_context

User = get_user_model()


class EssayPDFFlipbookView(LoginRequiredMixin, View):
    def get(self, request, essay_id, *args, **kwargs):
        import os

        from django.conf import settings
        from django.http import Http404

        # Buscar o Essay e usar o campo pdf, se disponível
        try:
            essay = Essay.objects.get(id=essay_id)

            if essay.pdf:
                # Verifica se o arquivo existe
                pdf_path = os.path.join(settings.MEDIA_ROOT, str(essay.pdf))
                if os.path.exists(pdf_path):
                    pdf_url = essay.pdf.url
                else:
                    raise Http404(
                        f"PDF da redação #{essay_id} não encontrado. O arquivo foi removido ou não existe."
                    )
            else:
                # Tenta o caminho padrão
                pdf_path = os.path.join(settings.MEDIA_ROOT, "pdfs", f"{essay_id}.pdf")
                if os.path.exists(pdf_path):
                    pdf_url = f"/media/pdfs/{essay_id}.pdf"
                else:
                    raise Http404(
                        f"PDF da redação #{essay_id} não foi enviado. Por favor, faça o upload do arquivo PDF primeiro."
                    )

        except Essay.DoesNotExist:
            raise Http404(f"Redação #{essay_id} não encontrada no sistema.")

        return render(
            request, "dashboard/pdf_flipbook.html", {"pdf_url": pdf_url, "essay": essay}
        )


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
            essays = (
                Essay.objects.filter(
                    status__in=[Essay.Status.SUBMITTED, Essay.Status.CORRECTED]
                )
                .select_related("student")
                .order_by("-created_at")[:20]
            )
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
            # Lista últimas redações do aluno (rascunhos, enviadas e corrigidas)
            ctx["recent_essays"] = (
                Essay.objects.filter(student=user).order_by("-created_at")
            )[:10]

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
        texto = request.POST.get("texto")
        titulo = request.POST.get("titulo")
        user = request.user
        pdf_file = request.FILES.get("pdf")

        essay_obj = Essay(
            student=user, title=titulo, text=texto, status=Essay.Status.SUBMITTED
        )
        if pdf_file:
            essay_obj.pdf = pdf_file
        essay_obj.save()

        # Gere o PDF automaticamente se não foi enviado
        if not pdf_file:
            essay_data = {"titulo": titulo, "texto": texto}
            pdf_path = generate_pdf(essay_data, essay_id=essay_obj.id)
            # Opcional: salvar o PDF gerado no campo pdf
            # with open(pdf_path, 'rb') as f:
            #     essay_obj.pdf.save(f"{essay_obj.id}.pdf", f, save=True)

        return redirect("dashboard:dashboard-role", role="teacher")

    def get(self, request, *args, **kwargs):
        # Exibe formulário simples para upload (pode ser removido se for 100% automático)
        return render(request, "dashboard/pdf_upload.html")


class StudentEssaySubmitView(LoginRequiredMixin, View):
    """
    View para processar submissão de redação do aluno via formulário HTML.
    Cria a redação e redireciona de volta ao dashboard com mensagem de sucesso.
    """

    def post(self, request, *args, **kwargs):
        # Verifica se o usuário é aluno
        if request.user.role != "student":
            messages.error(request, "Apenas alunos podem enviar redações.")
            return redirect("dashboard:dashboard")

        # Coleta dados do formulário
        title = request.POST.get("theme", "").strip()
        text = request.POST.get("text", "").strip()
        pdf_file = request.FILES.get("file")

        # Validação básica
        if not title or not text:
            messages.error(request, "Por favor, preencha o tema e o texto da redação.")
            return redirect("dashboard:dashboard-role", role="student")

        # Cria a redação
        try:
            essay = Essay.objects.create(
                student=request.user,
                title=title,
                text=text,
                status=Essay.Status.SUBMITTED,  # Marca como enviado para correção
            )

            # Se houver arquivo PDF, salva
            if pdf_file:
                essay.pdf = pdf_file
                essay.save()

            messages.success(
                request, f"✅ Redação '{title}' enviada com sucesso! ID: {essay.id}"
            )
        except Exception as e:
            messages.error(request, f"Erro ao enviar redação: {str(e)}")

        return redirect("dashboard:dashboard-role", role="student")
