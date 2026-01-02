# App Profiles - Perfis de Usuário

## 📋 Visão Geral

Gerencia informações adicionais de estudantes e professores através de perfis estendidos.

## 🎯 Models

### StudentProfile

```python
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    institution = models.CharField(max_length=200, blank=True)
    grade = models.CharField(max_length=50, blank=True)  # Série/Ano
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
```

### TeacherProfile

```python
class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    specialization = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    years_experience = models.IntegerField(default=0)
    phone = models.CharField(max_length=20, blank=True)
```

## 📡 API Endpoints

**Perfil do Aluno**
```http
GET /api/profiles/student/{user_id}/
PATCH /api/profiles/student/{user_id}/
```

**Perfil do Professor**
```http
GET /api/profiles/teacher/{user_id}/
PATCH /api/profiles/teacher/{user_id}/
```

## 🔗 Uso

```python
# Acessar perfil
if request.user.role == 'student':
    profile = request.user.student_profile
elif request.user.role == 'teacher':
    profile = request.user.teacher_profile
```
