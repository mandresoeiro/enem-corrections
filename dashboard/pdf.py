from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile


def generate_pdf(essay):
    html_string = render_to_string("pdf/correction.html", {"essay": essay})

    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    HTML(string=html_string).write_pdf(pdf_file.name)

    return pdf_file.name
