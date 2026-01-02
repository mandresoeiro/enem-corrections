# API Performance

## 📊 Visão Geral

API para métricas e análise de desempenho dos estudantes.

## 📡 Endpoints

### Métricas do Usuário Atual

```http
GET /api/performance/me/
Authorization: Bearer <access_token>
```

**Response 200 (Aluno):**
```json
{
  "role": "student",
  "user": {
    "id": 2,
    "username": "aluno1",
    "email": "aluno1@example.com"
  },
  "metrics": {
    "essays_total": 15,
    "essays_corrected": 12,
    "essays_pending": 3,
    "last_score": 850,
    "average_score": 780.5,
    "best_score": 920,
    "worst_score": 650
  },
  "competence_averages": {
    "c1": 165,
    "c2": 158,
    "c3": 152,
    "c4": 148,
    "c5": 157
  },
  "monthly_evolution": [
    {
      "month": "2025-01",
      "average": 720,
      "count": 4
    },
    {
      "month": "2025-02",
      "average": 780,
      "count": 5
    }
  ]
}
```

**Response 200 (Professor):**
```json
{
  "role": "teacher",
  "user": {
    "id": 3,
    "username": "prof1"
  },
  "metrics": {
    "pending_essays": 8,
    "corrections_done": 45,
    "students_count": 20,
    "average_correction_time": "2.5 dias"
  }
}
```

### Métricas do Aluno

```http
GET /api/performance/student/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `student_id`: ID do aluno (opcional, usa o próprio se não informado)
- `start_date`: Data inicial (formato: YYYY-MM-DD)
- `end_date`: Data final (formato: YYYY-MM-DD)

**Response 200:**
```json
{
  "essays_total": 15,
  "last_score": 850,
  "average_score": 780.5,
  "competence_history": [
    {
      "competence": 1,
      "scores": [160, 165, 170, 175, 180],
      "average": 170,
      "trend": "improving"
    },
    {
      "competence": 2,
      "scores": [150, 155, 160, 158, 160],
      "average": 156.6,
      "trend": "stable"
    }
  ],
  "recent_essays": [
    {
      "id": 15,
      "title": "Última Redação",
      "score": 850,
      "date": "2025-12-05"
    }
  ]
}
```

### Métricas do Professor

```http
GET /api/performance/teacher/
Authorization: Bearer <access_token>
```

**Response 200:**
```json
{
  "pending_essays": 8,
  "corrections_done": 45,
  "pending_list": [
    {
      "id": 20,
      "title": "Redação sobre Meio Ambiente",
      "student": "aluno5",
      "submitted_at": "2025-12-07T10:00:00Z"
    }
  ]
}
```

### Métricas Administrativas

```http
GET /api/performance/admin/
Authorization: Bearer <access_token>
```

**Response 200:**
```json
{
  "total_users": 150,
  "total_students": 120,
  "total_teachers": 10,
  "total_essays": 450,
  "essays_pending": 25,
  "essays_corrected": 400,
  "essays_draft": 25,
  "average_score_platform": 765.8,
  "top_students": [
    {
      "id": 5,
      "username": "aluno_destaque",
      "average_score": 920
    }
  ],
  "active_teachers": [
    {
      "id": 3,
      "username": "prof1",
      "corrections_count": 45
    }
  ]
}
```

## 📈 Evolução Mensal

```http
GET /api/performance/student/evolution/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `months`: Número de meses (default: 6)

**Response 200:**
```json
{
  "evolution": [
    {
      "month": "2025-07",
      "essays_count": 3,
      "average_score": 720,
      "competences": {
        "c1": 150,
        "c2": 145,
        "c3": 140,
        "c4": 138,
        "c5": 147
      }
    },
    {
      "month": "2025-08",
      "essays_count": 4,
      "average_score": 780,
      "competences": {
        "c1": 165,
        "c2": 158,
        "c3": 152,
        "c4": 148,
        "c5": 157
      }
    }
  ]
}
```

## 📊 Ranking

```http
GET /api/performance/ranking/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `limit`: Número de resultados (default: 10)
- `period`: Período (month/semester/year/all)

**Response 200:**
```json
{
  "period": "month",
  "ranking": [
    {
      "position": 1,
      "student": {
        "id": 5,
        "username": "aluno_top",
        "name": "Maria Silva"
      },
      "average_score": 920,
      "essays_count": 5
    },
    {
      "position": 2,
      "student": {
        "id": 8,
        "username": "aluno2",
        "name": "João Santos"
      },
      "average_score": 885,
      "essays_count": 4
    }
  ]
}
```

## 💡 Exemplos

### Python
```python
import requests

headers = {'Authorization': f'Bearer {token}'}

# Métricas do usuário atual
response = requests.get(
    'http://localhost:8000/api/performance/me/',
    headers=headers
)
metrics = response.json()

print(f"Total de redações: {metrics['metrics']['essays_total']}")
print(f"Média geral: {metrics['metrics']['average_score']}")
```

### JavaScript
```javascript
// Buscar métricas
const response = await fetch('http://localhost:8000/api/performance/me/', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const data = await response.json();

// Renderizar gráfico de evolução
renderChart(data.monthly_evolution);
```

## 🔒 Permissões

- `/me/`: Qualquer usuário autenticado
- `/student/`: Aluno vê apenas suas próprias métricas, professores/admins veem qualquer aluno
- `/teacher/`: Apenas professores
- `/admin/`: Apenas administradores
- `/ranking/`: Todos os autenticados

## ❌ Erros

**403 Forbidden:**
```json
{
  "detail": "Você não tem permissão para acessar estas métricas."
}
```

**404 Not Found:**
```json
{
  "detail": "Aluno não encontrado."
}
```
