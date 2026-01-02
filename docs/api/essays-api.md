# API Essays

## 📝 Visão Geral

API para gerenciamento de redações e correções.

## 📡 Endpoints

### Listar Redações

```http
GET /api/essays/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `status`: Filtrar por status (draft/submitted/corrected/returned)
- `student`: Filtrar por ID do aluno
- `page`: Número da página

**Response 200:**
```json
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "title": "Educação no Brasil",
      "student": {
        "id": 2,
        "username": "aluno1",
        "email": "aluno1@example.com"
      },
      "status": "corrected",
      "pdf": "/media/pdfs/1.pdf",
      "created_at": "2025-12-01T10:00:00Z",
      "score": {
        "c1": 180,
        "c2": 160,
        "c3": 170,
        "c4": 150,
        "c5": 160,
        "total": 820
      }
    }
  ]
}
```

### Criar Redação

```http
POST /api/essays/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

title=Título da Redação
text=Texto completo...
pdf=@arquivo.pdf
```

**Response 201:**
```json
{
  "id": 10,
  "title": "Título da Redação",
  "text": "Texto completo...",
  "status": "draft",
  "pdf": "/media/pdfs/10.pdf",
  "created_at": "2025-12-08T11:00:00Z"
}
```

### Detalhes da Redação

```http
GET /api/essays/{id}/
Authorization: Bearer <access_token>
```

**Response 200:**
```json
{
  "id": 1,
  "title": "Educação no Brasil",
  "text": "Texto completo da redação...",
  "student": {...},
  "status": "corrected",
  "pdf": "/media/pdfs/1.pdf",
  "score": {
    "c1": 180,
    "c2": 160,
    "c3": 170,
    "c4": 150,
    "c5": 160,
    "total": 820,
    "feedback": "Boa estrutura argumentativa...",
    "corrected_by": {
      "id": 3,
      "username": "prof1"
    }
  },
  "created_at": "2025-12-01T10:00:00Z"
}
```

### Atualizar Redação

```http
PATCH /api/essays/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Novo Título",
  "text": "Texto atualizado..."
}
```

**Response 200:**
```json
{
  "id": 1,
  "title": "Novo Título",
  "text": "Texto atualizado...",
  "status": "draft"
}
```

### Submeter para Correção

```http
POST /api/essays/{id}/submit/
Authorization: Bearer <access_token>
```

**Response 200:**
```json
{
  "id": 1,
  "status": "submitted",
  "message": "Redação enviada para correção com sucesso!"
}
```

### Corrigir Redação (Professor)

```http
POST /api/essays/{id}/correct/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "c1": 180,
  "c2": 160,
  "c3": 170,
  "c4": 150,
  "c5": 160,
  "feedback": "Excelente domínio da norma culta..."
}
```

**Response 200:**
```json
{
  "id": 1,
  "status": "corrected",
  "score": {
    "c1": 180,
    "c2": 160,
    "c3": 170,
    "c4": 150,
    "c5": 160,
    "total": 820,
    "feedback": "Excelente domínio da norma culta...",
    "corrected_by": 3
  }
}
```

### Deletar Redação

```http
DELETE /api/essays/{id}/
Authorization: Bearer <access_token>
```

**Response 204 No Content**

## 🎯 Competências ENEM

Cada competência é avaliada de 0 a 200 pontos:

- **C1**: Domínio da norma culta
- **C2**: Compreender a proposta
- **C3**: Selecionar e relacionar argumentos
- **C4**: Demonstrar conhecimento dos mecanismos linguísticos
- **C5**: Elaborar proposta de intervenção

**Total**: Soma das 5 competências (máximo 1000 pontos)

## ❌ Erros

**404 Not Found:**
```json
{
  "detail": "Redação não encontrada."
}
```

**400 Bad Request:**
```json
{
  "c1": ["O valor deve estar entre 0 e 200."],
  "title": ["Este campo é obrigatório."]
}
```

## 💡 Exemplos

### Python
```python
import requests

headers = {'Authorization': f'Bearer {token}'}

# Criar redação
files = {'pdf': open('redacao.pdf', 'rb')}
data = {
    'title': 'Minha Redação',
    'text': 'Texto completo...'
}
response = requests.post(
    'http://localhost:8000/api/essays/',
    headers=headers,
    data=data,
    files=files
)

# Submeter
essay_id = response.json()['id']
requests.post(
    f'http://localhost:8000/api/essays/{essay_id}/submit/',
    headers=headers
)
```

### JavaScript
```javascript
// Upload com FormData
const formData = new FormData();
formData.append('title', 'Minha Redação');
formData.append('text', 'Texto completo...');
formData.append('pdf', fileInput.files[0]);

const response = await fetch('http://localhost:8000/api/essays/', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData
});
```
