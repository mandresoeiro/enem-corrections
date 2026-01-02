# Variáveis de Ambiente (.env)

## 📄 Visão Geral

O projeto usa `python-decouple` para gerenciar variáveis de ambiente de forma segura. Todas as configurações sensíveis devem estar no arquivo `.env` na raiz do projeto.

## 🔧 Arquivo .env Completo

```env
# ============================================
# 🔐 SEGURANÇA DJANGO
# ============================================
SECRET_KEY=sua-chave-secreta-super-forte-aqui-com-50-caracteres
DEBUG=True

# Exemplo: localhost, 127.0.0.1, seu domínio
ALLOWED_HOSTS=127.0.0.1,localhost

# Ambiente: dev ou production
DJANGO_ENV=dev

# ============================================
# 📦 BANCO DE DADOS (DEV)
# ============================================
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# ============================================
# 📦 BANCO DE DADOS (PRODUÇÃO)
# Descomente quando estiver no Docker / Railway / Render
# ============================================
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=enem_db
# DB_USER=postgres
# DB_PASSWORD=sua-senha-segura-aqui
# DB_HOST=localhost
# DB_PORT=5432

# ============================================
# 🔐 SUPERUSER AUTOMÁTICO (createadmin)
# ============================================
DJANGO_ADMIN_EMAIL=admin@enempro.com
DJANGO_ADMIN_PASSWORD=Admin123!
DJANGO_ADMIN_USERNAME=admin

# ============================================
# 🔐 USUÁRIO ALUNO AUTOMÁTICO (createuser)
# ============================================
DJANGO_USER_EMAIL=aluno@enempro.com
DJANGO_USER_PASSWORD=Aluno123!
DJANGO_USER_USERNAME=aluno

# ============================================
# 🔐 USUÁRIO PROFESSOR AUTOMÁTICO (createuser)
# ============================================
DJANGO_TEACHER_EMAIL=prof@enempro.com
DJANGO_TEACHER_PASSWORD=Prof123!
DJANGO_TEACHER_USERNAME=prof

# ============================================
# 🔐 CONFIG JWT
# ============================================
JWT_ACCESS_MINUTES=30
JWT_REFRESH_DAYS=7

# ============================================
# 📧 EMAIL — PARA RESET DE SENHA, CONFIRMAÇÃO ETC
# Usar console email backend em DEV
# ============================================
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
EMAIL_USE_TLS=True

# ============================================
# 🌍 LOCALIZAÇÃO
# ============================================
LANGUAGE_CODE=pt-br
TIME_ZONE=America/Sao_Paulo
```

## 📋 Descrição das Variáveis

### Segurança Django

| Variável | Descrição | Exemplo | Obrigatória |
|----------|-----------|---------|-------------|
| `SECRET_KEY` | Chave secreta do Django (50+ caracteres) | `django-insecure-xyz123...` | ✅ |
| `DEBUG` | Modo debug (True/False) | `True` | ✅ |
| `ALLOWED_HOSTS` | Hosts permitidos (separados por vírgula) | `localhost,127.0.0.1` | ✅ |
| `DJANGO_ENV` | Ambiente (dev/production) | `dev` | ❌ |

### Banco de Dados

#### SQLite (Desenvolvimento)
| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `DB_ENGINE` | Engine SQLite | `django.db.backends.sqlite3` |
| `DB_NAME` | Nome do arquivo | `db.sqlite3` |

#### PostgreSQL (Produção)
| Variável | Descrição | Exemplo | Obrigatória |
|----------|-----------|---------|-------------|
| `DB_ENGINE` | Engine PostgreSQL | `django.db.backends.postgresql` | ✅ |
| `DB_NAME` | Nome do banco | `enem_db` | ✅ |
| `DB_USER` | Usuário do banco | `postgres` | ✅ |
| `DB_PASSWORD` | Senha do banco | `senha123` | ✅ |
| `DB_HOST` | Host do banco | `localhost` ou IP | ✅ |
| `DB_PORT` | Porta do banco | `5432` | ❌ |

### Usuários Automáticos

Credenciais para comandos de gerenciamento (`createadmin`, `createuser`):

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `DJANGO_ADMIN_EMAIL` | Email do admin | `admin@example.com` |
| `DJANGO_ADMIN_PASSWORD` | Senha do admin | `Admin123!` |
| `DJANGO_ADMIN_USERNAME` | Username do admin | `admin` |
| `DJANGO_USER_EMAIL` | Email do aluno | `aluno@example.com` |
| `DJANGO_USER_PASSWORD` | Senha do aluno | `Aluno123!` |
| `DJANGO_USER_USERNAME` | Username do aluno | `aluno` |

### JWT (Tokens)

| Variável | Descrição | Padrão | Tipo |
|----------|-----------|--------|------|
| `JWT_ACCESS_MINUTES` | Tempo de vida do access token (minutos) | `30` | int |
| `JWT_REFRESH_DAYS` | Tempo de vida do refresh token (dias) | `7` | int |

### Email

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `EMAIL_BACKEND` | Backend de email | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST` | Servidor SMTP | `smtp.gmail.com` |
| `EMAIL_PORT` | Porta SMTP | `587` |
| `EMAIL_HOST_USER` | Email remetente | `seu_email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Senha/App password | `senha-de-app` |
| `EMAIL_USE_TLS` | Usar TLS | `True` |

### Localização

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `LANGUAGE_CODE` | Idioma do sistema | `pt-br` |
| `TIME_ZONE` | Fuso horário | `America/Sao_Paulo` |

## 🔒 Segurança e Boas Práticas

### ✅ Faça

1. **Nunca commite o arquivo .env**
   ```bash
   # .gitignore já deve conter:
   .env
   ```

2. **Use senhas fortes**
   ```python
   # Gerar SECRET_KEY
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **Crie um .env.example**
   ```bash
   cp .env .env.example
   # Remova valores sensíveis do .env.example
   git add .env.example
   ```

4. **Use diferentes .env por ambiente**
   ```
   .env.dev
   .env.prod
   .env.test
   ```

### ❌ Não Faça

1. Não use valores padrão em produção
2. Não compartilhe .env em mensagens/emails
3. Não use a mesma SECRET_KEY em dev e prod
4. Não deixe DEBUG=True em produção

## 📝 Configuração Inicial

### 1. Copie o exemplo

```bash
cp .env.example .env
```

### 2. Gere uma SECRET_KEY

```bash
poetry run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Configure o banco de dados

**Desenvolvimento (SQLite):**
```env
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

**Produção (PostgreSQL):**
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=enem_db
DB_USER=postgres
DB_PASSWORD=senha-segura
DB_HOST=localhost
DB_PORT=5432
```

### 4. Configure email (opcional em dev)

**Desenvolvimento:**
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**Produção (Gmail):**
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=senha-de-app-do-gmail
EMAIL_USE_TLS=True
```

## 🔧 Uso no Código

### Lendo variáveis

```python
from decouple import config

# String
secret_key = config('SECRET_KEY')

# Boolean
debug = config('DEBUG', default=False, cast=bool)

# Integer
jwt_minutes = config('JWT_ACCESS_MINUTES', default=30, cast=int)

# Lista (separada por vírgula)
allowed_hosts = config('ALLOWED_HOSTS', default='').split(',')
```

### Valores padrão

Sempre forneça valores padrão para variáveis opcionais:

```python
language_code = config('LANGUAGE_CODE', default='pt-br')
time_zone = config('TIME_ZONE', default='America/Sao_Paulo')
```

## 🐳 Docker e Deploy

### Docker Compose

```yaml
services:
  web:
    env_file:
      - .env
    environment:
      - DJANGO_ENV=production
```

### Railway / Render

Configure as variáveis no painel de controle da plataforma:

1. Acesse as configurações do projeto
2. Adicione cada variável individualmente
3. Não precisa do arquivo .env (use variáveis de ambiente da plataforma)

### Heroku

```bash
heroku config:set SECRET_KEY="sua-chave-aqui"
heroku config:set DEBUG=False
heroku config:set DB_ENGINE=django.db.backends.postgresql
# ... outras variáveis
```

## 🧪 Testes

Para testes, sobrescreva variáveis:

```bash
# Linux/Mac
DEBUG=False DJANGO_ENV=test poetry run pytest

# Windows PowerShell
$env:DEBUG="False"; $env:DJANGO_ENV="test"; poetry run pytest
```

Ou crie `.env.test`:

```env
DEBUG=False
DJANGO_ENV=test
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=:memory:
```

## 📚 Referências

- [python-decouple docs](https://github.com/henriquebastos/python-decouple)
- [Django Settings Best Practices](https://docs.djangoproject.com/en/5.1/topics/settings/)
- [12 Factor App](https://12factor.net/config)
