# 👤 Accounts – Autenticação e Usuários

O app **accounts** gerencia todo o fluxo de autenticação, autorização e gestão de usuários do sistema.
Ele implementa um **modelo customizado de usuário**, suporte a **roles**, comandos de administração e integrações com **dj-rest-auth + SimpleJWT**.

---

# 🗂️ Estrutura do App

```text
accounts/
├── models.py              # Modelo CustomUser
├── serializers.py         # Serializers da API
├── views.py               # Endpoints REST
├── urls.py                # Rotas da API
├── admin.py               # Configuração do Django Admin
├── management/
│   └── commands/
│       ├── createadmin.py
│       ├── createsuperuser.py
│       └── createuser.py
└── templates/
    └── accounts/
        ├── login.html
        ├── register.html
```

---

# 🧬 Modelo de Usuário – `CustomUser`

O modelo estende **AbstractUser**, mas adiciona:

- Login por **email**
- Campo **role** (student/teacher/admin)
- Auditoria (`created_at`, `updated_at`)
- Permite autenticação moderna via JWT

---

## 🔍 Código-base do Modelo

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Aluno"
        TEACHER = "teacher", "Professor"
        ADMIN = "admin", "Administrador"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text="Papel principal do usuário"
    )

    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
```

---

# ✔ Campos Principais

| Campo        | Descrição                              | Origem          |
|--------------|------------------------------------------|------------------|
| `username`   | Nome de usuário                          | AbstractUser     |
| `email`      | Identificador principal (único)          | CustomUser       |
| `password`   | Senha hasheada                           | AbstractUser     |
| `role`       | Papel do usuário no sistema              | CustomUser       |
| `is_active`  | Usuário ativo                            | AbstractUser     |
| `is_staff`   | Permissões administrativas               | AbstractUser     |
| `date_joined`| Data de criação da conta                 | AbstractUser     |

---

# 📡 Serializers

### 🧩 `UserSerializer`

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'role',
            'first_name', 'last_name', 'is_active'
        ]
        read_only_fields = ['id', 'role']
```

---

### 🧩 `RegisterSerializer`

```python
class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Senhas não coincidem")
        return data
```

---

# 🧠 Views e Fluxo de Autenticação

O fluxo utiliza `dj-rest-auth` + SimpleJWT.

| View           | URL                      | Descrição                        |
|----------------|--------------------------|----------------------------------|
| Login          | `/auth/login/`           | Autenticação por email + senha   |
| Logout         | `/auth/logout/`          | Encerra sessão JWT               |
| Registro       | `/auth/registration/`    | Criação de usuário               |
| Refresh Token  | `/auth/token/refresh/`   | Gera novo access token           |
| List Users     | `/api/accounts/users/`   | Lista usuários (JWT protegido)   |

---

# 🔐 Permissões e Roles

### Helpers:

```python
user.is_student
user.is_teacher
user.is_admin
```

### DRF Permission Example:

```python
class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'teacher'
```

---

# 🛠️ Comandos de Gerenciamento

### Criar admin via .env

```bash
poetry run python manage.py createadmin
```

### Criar superusuário padrão

```bash
poetry run python manage.py createsuperuser
```

### Criar usuários com roles

```bash
poetry run python manage.py createuser --role=teacher
```

---

# 📊 Testes (pytest)

```python
def test_create_user():
    user = CustomUser.objects.create_user(
        username='test',
        email='test@example.com',
        password='test123',
        role='student'
    )
    assert user.role == 'student'
    assert user.check_password('test123')
```

---

# 🔗 Integrações

- SimpleJWT
- dj-rest-auth
- django-allauth (futuro)
- app profiles (para estender dados do usuário)

---

# 📝 Boas Práticas

1. Sempre usar `get_user_model()`
2. Nunca salvar senhas sem hashing
3. Roles devem ser comparadas por `User.Role.X`
4. Usar UUID em produção (recomendado)
5. Proteger login com rate limiting
6. Documentar autenticação no frontend
