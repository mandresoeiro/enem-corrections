"""
===============================================================
🔧 BASE SETTINGS — Django 5.1 (LTS)
===============================================================
Este arquivo define TODA a fundação do seu projeto:

- Diretórios base
- Segurança
- Apps instalados
- Middlewares
- Templates
- Autenticação (JWT + dj-rest-auth + allauth)
- Django REST Framework
- Internacionalização
- Static & Media
- Configurações do Jazzmin (tema do Admin)

⚠️ IMPORTANTE:
NENHUMA informação sensível deve ser colocada aqui.
Tudo deve vir do .env via python-decouple.
===============================================================
"""

from pathlib import Path
from datetime import timedelta
from decouple import config
import os


# ==============================================================
# 0. DIRETÓRIOS BÁSICOS
# ==============================================================

"""
Exemplo de estrutura esperada:

backend/
│── apps/
│── core/
│   └── settings/
│       ├── base.py  ← estamos aqui
│       ├── dev.py
│       └── prod.py
"""

# BASE_DIR resolve o diretório raiz do projeto Django
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ==============================================================
# 1. SEGURANÇA BÁSICA
# ==============================================================

# Nunca deixe SECRET_KEY exposta no código → usar .env
SECRET_KEY = config("SECRET_KEY", default="unsafe-secret-key")

# Debug deve ser DESATIVADO no ambiente de produção
DEBUG = False

# Em produção: configure domínios reais
# Ex: ["api.soeirotech.com", "backend.enempro.com"]
ALLOWED_HOSTS = ["*"]  # somente para desenvolvimento


# ==============================================================
# 2. CONFIGURAÇÃO PRINCIPAL DE URLS
# ==============================================================

ROOT_URLCONF = "core.urls"


# ==============================================================
# 3. APLICAÇÕES INSTALADAS
# ==============================================================

INSTALLED_APPS = [
    # ------------------------------
    # Admin moderno (Jazzmin)
    # ------------------------------
    "jazzmin",  # deve vir antes do django.contrib.admin

    # ------------------------------
    # Apps nativos Django
    # ------------------------------
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # necessário para django-allauth

    # ------------------------------
    # Apps de terceiros
    # ------------------------------
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    # ------------------------------
    # Apps internos do projeto
    # ------------------------------
    "accounts",
    "profiles",
    "essays",
    "performance",
    "dashboard",
    "visual",
]

# django-allauth exige que exista um SITE_ID
SITE_ID = 1


# ==============================================================
# 4. MIDDLEWARES
# ==============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    # Proteção contra ataques CSRF
    "django.middleware.csrf.CsrfViewMiddleware",

    # Autenticação de usuário
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # Necessário para o allauth (senão dá erro)
    "allauth.account.middleware.AccountMiddleware",

    # Mensagens → message.success(), message.error()
    "django.contrib.messages.middleware.MessageMiddleware",

    # Proteção contra clickjacking
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==============================================================
# 5. MODELO DE USUÁRIO CUSTOMIZADO
# ==============================================================

"""
Sempre utilize um CustomUser.
Isso evita limitações futuras quando quiser adicionar campos.
"""
AUTH_USER_MODEL = "accounts.CustomUser"


# ==============================================================
# 6. TEMPLATES
# ==============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        # Locais adicionais para templates globais
        "DIRS": [
            BASE_DIR / "visual" / "templates",
            BASE_DIR / "dashboard" / "templates",
        ],

        # Permite buscar templates automaticamente dentro de cada app
        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # permite {{ request.user }}
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ==============================================================
# 7. BANCO DE DADOS (SQLite padrão)
# ==============================================================

"""
Em desenvolvimento: SQLite
Em produção: configure PostgreSQL no prod.py
"""

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ==============================================================
# 8. ARQUIVOS ESTÁTICOS (CSS / JS)
# ==============================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "visual" / "static",  # onde ficam Tailwind e assets
]

STATIC_ROOT = BASE_DIR / "staticfiles"  # pasta final para collectstatic


# ==============================================================
# 9. ARQUIVOS DE MÍDIA (UPLOADS)
# ==============================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

"""
Todos os uploads (imagens, PDFs, redações, etc)
serão armazenados em /media/
"""


# ==============================================================
# 10. AUTENTICAÇÃO + DRF + JWT
# ==============================================================

# Redirecionamentos de login/logout
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# Serializer customizado para registro via API
REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "accounts.serializers.CustomRegisterSerializer",
}

# Ativa JWT no dj-rest-auth
REST_USE_JWT = True

# Configurações JWT (tempo de expiração)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# ==============================================================
# 11. CONFIGURAÇÕES ALLAUTH
# ==============================================================

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"  # Em produção: "mandatory"


# ==============================================================
# 12. INTERNACIONALIZAÇÃO
# ==============================================================

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True


# ==============================================================
# 13. WSGI / ASGI
# ==============================================================

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"


# ==============================================================
# 14. JAZZMIN — Tema Profissional do Django Admin
# ==============================================================

JAZZMIN_SETTINGS = {
    "site_title": "ENEM Corrections Admin",
    "site_header": "Correções ENEM",
    "site_brand": "ENEM Pro",
    "welcome_sign": "Bem-vindo ao Painel Administrativo ENEM Pro",
    "copyright": "SoeiroTech © 2025",
    "show_sidebar": True,
    "navigation_expanded": True,
    "show_ui_builder": False,

    # Ordem dos apps no menu lateral
    "order_with_respect_to": [
        "accounts",
        "profiles",
        "essays",
        "performance",
        "dashboard",
    ],

    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index"},
        {"name": "Github", "url": "https://github.com/soeirotech"},
    ],

    # Ícones (Font Awesome)
    "icons": {
        "accounts.CustomUser": "fas fa-user",
        "profiles.StudentProfile": "fas fa-user-graduate",
        "profiles.TeacherProfile": "fas fa-chalkboard-teacher",
        "essays.Essay": "fas fa-file-alt",
        "essays.CompetenceScore": "fas fa-star",
        "performance": "fas fa-chart-line",
        "dashboard": "fas fa-tachometer-alt",
    },

    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-file",
    "site_color": "green",
}


# ==============================================================
# 15. PALETA DE CORES PERSONALIZADA
# ==============================================================

JAZZMIN_COLORS = {
    "primary": "#0f766e",
    "secondary": "#064e3b",
    "accent": "#10b981",
    "dark": "#022c22",
    "light": "#f0fdfa",
}


# ==============================================================
# 16. UI TWEAKS — Ajustes Visuais do Admin
# ==============================================================

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",
    "navbar": "navbar-dark",
    "accent": "accent-green",
    "navbar_small_text": False,
    "sidebar_small_text": False,
    "brand_small_text": False,
    "footer_small_text": False,
}
