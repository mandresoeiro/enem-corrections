# Settings Django

## 📁 Estrutura de Settings

O projeto utiliza configurações modularizadas em `core/settings/`:

```
core/settings/
├── __init__.py      # Detecta ambiente e carrega o settings correto
├── base.py          # Configurações comuns a todos os ambientes
├── dev.py           # Configurações de desenvolvimento
└── prod.py          # Configurações de produção
```

## ⚙️ base.py - Configurações Base

### Aplicações Instaladas

```python
INSTALLED_APPS = [
    # Admin customizado
    'jazzmin',

    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'drf_spectacular',

    # Apps do projeto
    'accounts',
    'profiles',
    'essays',
    'performance',
    'dashboard',
    'visual',
]
```

### Autenticação

```python
# Model de usuário customizado
AUTH_USER_MODEL = 'accounts.CustomUser'

# Backend de autenticação
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Configurações de autenticação
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
```

### REST Framework

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

### JWT (JSON Web Tokens)

```python
from datetime import timedelta
from decouple import config

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(config('JWT_ACCESS_MINUTES', default=30))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(config('JWT_REFRESH_DAYS', default=7))),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

REST_USE_JWT = True
JWT_AUTH_COOKIE = 'access-token'
JWT_AUTH_REFRESH_COOKIE = 'refresh-token'
```

### Django Allauth

```python
SITE_ID = 1

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
```

### Internacionalização

```python
from decouple import config

LANGUAGE_CODE = config('LANGUAGE_CODE', default='pt-br')
TIME_ZONE = config('TIME_ZONE', default='America/Sao_Paulo')
USE_I18N = True
USE_TZ = True
```

### Arquivos Estáticos e Media

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Email

```python
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
```

## 🔧 dev.py - Desenvolvimento

```python
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Banco de dados SQLite para desenvolvimento
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Django Debug Toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']

# Logs detalhados
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

## 🚀 prod.py - Produção

```python
from .base import *
from decouple import config

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files (WhiteNoise)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

## 🔀 Seleção Automática de Ambiente

O arquivo `core/settings/__init__.py` detecta automaticamente o ambiente:

```python
import os
from decouple import config

# Lê a variável DJANGO_ENV do .env
environment = config('DJANGO_ENV', default='dev')

if environment == 'production':
    from .prod import *
else:
    from .dev import *
```

## 🎨 Jazzmin (Admin Customizado)

```python
JAZZMIN_SETTINGS = {
    "site_title": "ENEM Corrections",
    "site_header": "ENEM Corrections Admin",
    "site_brand": "ENEM Corrections",
    "welcome_sign": "Bem-vindo ao painel administrativo",
    "copyright": "ENEM Corrections © 2025",
    "show_ui_builder": False,
}
```

## 📊 DRF Spectacular (API Docs)

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'ENEM Corrections API',
    'DESCRIPTION': 'API REST para gestão de correções de redações ENEM',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

## 🔐 Configurações de Segurança

### SECRET_KEY

**Nunca** commite a SECRET_KEY! Use o `.env`:

```python
SECRET_KEY = config('SECRET_KEY')
```

Gere uma nova chave:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### CORS (se usar frontend separado)

```python
# Adicione ao INSTALLED_APPS
'corsheaders',

# Adicione ao MIDDLEWARE
'corsheaders.middleware.CorsMiddleware',

# Configure origins permitidos
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
]
```

## 🧪 Settings para Testes

Crie `core/settings/test.py`:

```python
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
```

Execute testes com:

```bash
DJANGO_ENV=test poetry run pytest
```

## 📝 Checklist de Configuração

### Desenvolvimento
- [ ] `DEBUG = True`
- [ ] SQLite configurado
- [ ] Email backend = console
- [ ] ALLOWED_HOSTS = localhost

### Produção
- [ ] `DEBUG = False`
- [ ] PostgreSQL configurado
- [ ] SECRET_KEY forte e única
- [ ] ALLOWED_HOSTS correto
- [ ] SSL/HTTPS habilitado
- [ ] Whitenoise configurado
- [ ] Email SMTP real configurado
- [ ] Logs configurados
