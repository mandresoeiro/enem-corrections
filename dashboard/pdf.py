from django.template.loader import render_to_string
from weasyprint import HTML
import os
from django.conf import settings


def generate_pdf(essay, essay_id=None):
    html_string = render_to_string("pdf/correction.html", {"essay": essay})

    # Caminho para salvar o PDF
    pdf_dir = os.path.join(settings.MEDIA_ROOT, "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    filename = f"{essay_id or 'temp'}.pdf"
    pdf_path = os.path.join(pdf_dir, filename)
    HTML(string=html_string).write_pdf(pdf_path)

    return pdf_path
