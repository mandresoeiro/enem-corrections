# Arquitetura do Sistema

## 📐 Visão Geral

O ENEM Corrections segue uma arquitetura modular baseada em **Django Apps**, com separação clara de responsabilidades e uma API REST completa.

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend / Cliente                    │
│  (Django Templates + TailwindCSS + Fetch API)           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    Django URLs Router                    │
│              (core/urls.py - Roteamento)                │
└─────────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┴─────────────────┐
        ↓                                     ↓
┌──────────────────┐              ┌──────────────────────┐
│  Django Views    │              │  Django REST API     │
│  (Templates)     │              │  (ViewSets/APIView)  │
└──────────────────┘              └──────────────────────┘
        ↓                                     ↓
┌─────────────────────────────────────────────────────────┐
│                    Business Logic                        │
│  (Models, Services, Serializers, Permissions)           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  Database (PostgreSQL/SQLite)            │
└─────────────────────────────────────────────────────────┘
```

## 🧩 Estrutura de Apps

### **accounts** - Autenticação e Usuários
- Model customizado de usuário com campo `role` (student/teacher/admin)
- Autenticação JWT com dj-rest-auth
- Comandos de gerenciamento: `createadmin`, `createsuperuser`, `createuser`
- Serializers para registro e login

### **profiles** - Perfis de Usuário
- `StudentProfile`: Dados adicionais de alunos (instituição, série, etc)
- `TeacherProfile`: Dados de professores (especialização, bio, etc)
- Relacionamento OneToOne com CustomUser

### **essays** - Redações e Correções
- `Essay`: Modelo principal de redações
  - Estados: draft, submitted, corrected, returned
  - Upload de PDF
  - Relacionamento com aluno
- `CompetenceScore`: Notas das 5 competências ENEM (C1-C5)
  - Pontuação de 0 a 200 por competência
  - Total máximo: 1000 pontos
  - Relacionamento com corretor

### **performance** - Métricas e Analytics
- `StudentPerformance`: Histórico de desempenho
- `CompetenceHistory`: Evolução por competência
- `MonthlyEvolution`: Evolução mensal
- APIs para dashboards e relatórios

### **dashboard** - Interface Visual
- Views baseadas em templates Django
- Dashboards diferenciados por role
- Upload de redações
- Visualização de PDFs (flipbook)
- Cards e métricas visuais

### **visual** - Componentes Reutilizáveis
- Templates base
- Componentes de UI (cards, buttons, etc)
- Layouts compartilhados

## 🔐 Sistema de Autenticação

### Fluxo de Autenticação

```
1. Usuário faz login → /accounts/login/
2. Django valida credenciais
3. Sistema cria sessão
4. Usuário é redirecionado para dashboard com base no role
```

### Autenticação API (JWT)

```
1. POST /auth/login/ → {email, password}
2. Sistema retorna {access, refresh, user}
3. Cliente usa access token no header: Authorization: Bearer <token>
4. Token expira após JWT_ACCESS_MINUTES (padrão: 30 min)
5. Refresh com POST /auth/token/refresh/
```

### Roles e Permissões

- **student**: Pode criar redações, ver suas próprias notas
- **teacher**: Pode corrigir redações, ver todas as submissões
- **admin**: Acesso total ao sistema

## 🗄️ Modelo de Dados

### Principais Relacionamentos

```
CustomUser (1) ──── (1) StudentProfile
CustomUser (1) ──── (1) TeacherProfile

CustomUser (1) ──── (N) Essay (student)
CustomUser (1) ──── (N) CompetenceScore (corrected_by)

Essay (1) ──── (1) CompetenceScore
Essay (1) ──── (N) StudentPerformance
```

### Status de Redação

- **draft**: Rascunho não enviado
- **submitted**: Enviada para correção
- **corrected**: Corrigida pelo professor
- **returned**: Devolvida ao aluno com feedback

## 🌐 API REST

### Endpoints Principais

**Autenticação**
- `POST /auth/login/` - Login
- `POST /auth/logout/` - Logout
- `POST /auth/token/refresh/` - Refresh token
- `POST /auth/registration/` - Registro

**Accounts**
- `GET /api/accounts/users/` - Listar usuários
- `GET /api/accounts/users/{id}/` - Detalhes do usuário
- `PATCH /api/accounts/users/{id}/` - Atualizar usuário

**Essays**
- `GET /api/essays/` - Listar redações
- `POST /api/essays/` - Criar redação
- `GET /api/essays/{id}/` - Detalhes da redação
- `PATCH /api/essays/{id}/` - Atualizar redação
- `POST /api/essays/{id}/submit/` - Submeter para correção

**Performance**
- `GET /api/performance/me/` - Métricas do usuário atual
- `GET /api/performance/student/` - Métricas do aluno
- `GET /api/performance/teacher/` - Métricas do professor
- `GET /api/performance/admin/` - Métricas administrativas

## 🎨 Frontend

### Tecnologias
- **Templates**: Django Template Language
- **CSS**: TailwindCSS (via CDN ou build)
- **JavaScript**: Vanilla JS + Fetch API
- **Ícones**: SVG inline

### Estrutura de Templates

```
dashboard/templates/
├── base.html                  # Template base
├── dashboard/
│   ├── index.html            # Dashboard principal
│   ├── teacher_dashboard.html
│   ├── student_dashboard.html
│   ├── admin_dashboard.html
│   ├── pdf_flipbook.html
│   └── components/
│       ├── cards_admin.html
│       ├── cards_student.html
│       └── ...
```

## 📦 Dependências Principais

```toml
django = "^5.1"
djangorestframework = "^3.16"
dj-rest-auth = "^7.0"
django-allauth = "^65.0"
djangorestframework-simplejwt = "^5.5"
psycopg2-binary = "^2.9"  # PostgreSQL
python-decouple = "^3.8"   # Env vars
weasyprint = "^66.0"       # PDF generation
django-jazzmin = "^3.0"    # Admin UI
```

## 🚀 Deploy

### Requisitos de Produção
- Python 3.12+
- PostgreSQL 12+
- Nginx (servidor web)
- Gunicorn (WSGI server)
- Redis (cache e sessões - opcional)

### Variáveis de Ambiente Essenciais
```env
DEBUG=False
SECRET_KEY=<chave-forte-aqui>
ALLOWED_HOSTS=seu-dominio.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=enem_db
DB_USER=postgres
DB_PASSWORD=senha-segura
DB_HOST=localhost
DB_PORT=5432
```

### Comandos de Deploy
```bash
# Coletar arquivos estáticos
poetry run python manage.py collectstatic --noinput

# Executar migrações
poetry run python manage.py migrate

# Criar superusuário
poetry run python manage.py createsuperuser

# Iniciar com Gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

## 🧪 Testes

```bash
# Rodar todos os testes
poetry run pytest

# Testes com coverage
poetry run pytest --cov

# Testes de um app específico
poetry run pytest accounts/tests/
```

## 📊 Performance e Otimização

### Queries Otimizadas
- Uso de `select_related()` para ForeignKeys
- Uso de `prefetch_related()` para ManyToMany
- Índices em campos frequentemente consultados

### Cache
- Cache de views com `@cache_page`
- Cache de queries com `cache.get()`/`cache.set()`

### Pagination
- Todas as listas usam pagination (padrão: 20 itens)
- Suporte a `?page=N` na API

## 🔒 Segurança

- CSRF protection habilitado
- XSS protection nos templates
- SQL Injection prevention (ORM)
- JWT com expiração configurável
- HTTPS obrigatório em produção
- Rate limiting na API (planejado)

## 📈 Monitoramento

- Healthcheck endpoint: `/health/`
- Logs estruturados
- Django Debug Toolbar (desenvolvimento)
- Sentry integration (planejado)
