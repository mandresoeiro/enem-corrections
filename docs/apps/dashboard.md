# App Dashboard - Interface Visual

## 📋 Visão Geral

Interface visual com dashboards diferenciados por role (aluno, professor, admin).

## 🎨 Views

### DashboardHomeView

**URL:** `/` ou `/dashboard/{role}/`
**Template:** `dashboard/index.html`

Detecta o role do usuário e renderiza o dashboard apropriado.

### EssayPDFUploadView

**URL:** `/dashboard/pdf/`
**Template:** `dashboard/pdf_upload.html`

Permite upload de PDFs de redações.

### EssayPDFFlipbookView

**URL:** `/dashboard/pdf/flipbook/{essay_id}/`
**Template:** `dashboard/pdf_flipbook.html`

Visualiza PDFs de redações.

## 📁 Templates

```
dashboard/templates/
├── dashboard/
│   ├── index.html                 # Dashboard principal
│   ├── student_dashboard.html     # Dashboard do aluno
│   ├── teacher_dashboard.html     # Dashboard do professor
│   ├── admin_dashboard.html       # Dashboard do admin
│   ├── pdf_upload.html           # Upload de PDF
│   ├── pdf_flipbook.html         # Visualizador de PDF
│   ├── base.html                 # Template base
│   └── components/
│       ├── cards_student.html
│       ├── cards_teacher.html
│       └── cards_admin.html
```

## 🎯 Contexto do Dashboard

```python
{
    'role': 'student',  # ou 'teacher', 'admin'
    'user': request.user,
    'metrics': {
        'title': 'Dashboard do Aluno',
        'essays_total': 10,
        'last_score': 850,
        'average_score': 780
    },
    'essays': [...],  # Lista de redações
    'pending_essays_count': 3,
    'corrected_essays_count': 7
}
```

## 🎨 Componentes

- **Cards**: Métricas visuais
- **Tabelas**: Listagem de redações
- **Gráficos**: Evolução de desempenho (planejado)
- **Modais**: Feedback e correções
