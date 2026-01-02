# App Performance - Métricas

## 📋 Visão Geral

Calcula e armazena métricas de desempenho dos estudantes.

## 🎯 Models

### StudentPerformance

```python
class StudentPerformance(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    essay = models.ForeignKey(Essay, on_delete=models.CASCADE)
    total_score = models.IntegerField()
    average_competence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### CompetenceHistory

```python
class CompetenceHistory(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    competence_number = models.IntegerField(choices=[(1,'C1'),(2,'C2'),(3,'C3'),(4,'C4'),(5,'C5')])
    score = models.IntegerField()
    essay = models.ForeignKey(Essay, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

### MonthlyEvolution

```python
class MonthlyEvolution(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    month = models.DateField()
    average_score = models.FloatField()
    essays_count = models.IntegerField()
```

## 📡 API Endpoints

```http
GET /api/performance/me/            # Métricas do usuário atual
GET /api/performance/student/       # Métricas do aluno
GET /api/performance/teacher/       # Métricas do professor
GET /api/performance/admin/         # Métricas administrativas
```

## 📊 Exemplo de Resposta

```json
{
  "essays_total": 15,
  "last_score": 880,
  "average_score": 750.5,
  "competence_averages": {
    "c1": 160,
    "c2": 155,
    "c3": 150,
    "c4": 145,
    "c5": 140
  }
}
```
