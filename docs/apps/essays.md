# App Essays - Redações

## 📋 Visão Geral

Gerencia redações, submissões e correções baseadas nas 5 competências do ENEM.

## 🎯 Models

### Essay

```python
class Essay(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Rascunho'
        SUBMITTED = 'submitted', 'Enviada'
        CORRECTED = 'corrected', 'Corrigida'
        RETURNED = 'returned', 'Devolvida'

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### CompetenceScore

```python
class CompetenceScore(models.Model):
    essay = models.OneToOneField(Essay, on_delete=models.CASCADE)
    corrected_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    c1 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    c2 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    c3 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    c4 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    c5 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_score(self):
        return self.c1 + self.c2 + self.c3 + self.c4 + self.c5
```

## 📡 API Endpoints

```http
GET /api/essays/                    # Listar redações
POST /api/essays/                   # Criar redação
GET /api/essays/{id}/               # Detalhes
PATCH /api/essays/{id}/             # Atualizar
DELETE /api/essays/{id}/            # Deletar
POST /api/essays/{id}/submit/       # Submeter para correção
POST /api/essays/{id}/correct/      # Corrigir (professor)
```

## 🎨 Views HTML

- `/dashboard/pdf/` - Upload de PDF
- `/dashboard/pdf/flipbook/{id}/` - Visualizar PDF
