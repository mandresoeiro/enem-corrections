"""
Base settings para Django 5.1 LTS.

Este arquivo define:
- apps comuns ao projeto
- middlewares
- templates
- DRF
- JWT
- allauth
- internacionalização
- caminhos básicos

⚠️ Este arquivo NÃO deve conter segredos (use .env).
"""

from pathlib import Path
from datetime import timedelta
import os
from decouple import config


# -----------------------------------------------------------
# 0. Diretórios básicos
# -----------------------------------------------------------

# EXEMPLO:
# Se este arquivo estiver em:
# backend/core/settings/base.py
# BASE_DIR vira: backend/
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# -----------------------------------------------------------
# 1. Segurança
# -----------------------------------------------------------

# SECRET_KEY deve vir do .env → NUNCA coloque no código.
# EXEMPLO .env:
# SECRET_KEY=uma_chave_grande_aleatoria
SECRET_KEY = config("SECRET_KEY", default="unsafe-secret-key")

# DEBUG deve ser True apenas em ambiente dev.py
DEBUG = False

# EXEMPLO em produção:
# ALLOWED_HOSTS = ["suaapi.com", "www.suaapi.com"]
ALLOWED_HOSTS = ["*"]  # liberar tudo só em dev/teste

# Onde está o arquivo principal de URLs do projeto
ROOT_URLCONF = "core.urls"


# -----------------------------------------------------------
# 2. Aplicações instaladas
# -----------------------------------------------------------

INSTALLED_APPS = [
    # Interface moderna para o Django Admin
    # ❗ MUST COME BEFORE "django.contrib.admin"
    "jazzmin",
    # -----------------------------
    # APPS NATIVOS DO DJANGO
    # -----------------------------
    "django.contrib.admin",  # painel administrativo
    "django.contrib.auth",  # autenticação
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # necessário pro allauth
    # -----------------------------
    # APPS DE TERCEIROS
    # -----------------------------
    "rest_framework",  # Django REST Framework
    "rest_framework.authtoken",  # Token API simples
    "rest_framework_simplejwt",  # JWT tokens
    "dj_rest_auth",  # login/logout via API
    "dj_rest_auth.registration",  # registro via API
    "allauth",  # core do allauth
    "allauth.account",  # autenticação
    "allauth.socialaccount",  # login social (opcional)
    # -----------------------------
    # APPS DO PROJETO
    # -----------------------------
    "accounts",
    "profiles",
    "essays",
    "performance",
    "dashboard",
    "visual",
]

# EXEMPLO: allauth precisa disso ou dá erro “Site matching query does not exist”
SITE_ID = 1


# -----------------------------------------------------------
# 3. Middlewares
# -----------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # Protege contra ataques CSRF (Forms e Session Auth)
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # ✔ Necessário para django-allauth funcionar
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# -----------------------------------------------------------
# 4. Modelo de usuário customizado
# -----------------------------------------------------------

# EXEMPLO:
# Em accounts/models.py você deve ter class CustomUser(AbstractUser)
AUTH_USER_MODEL = "accounts.CustomUser"


# -----------------------------------------------------------
# 5. Templates (HTML)
# -----------------------------------------------------------

"""
DIRS = locais onde ficam os seus templates globais.

EXEMPLO:
visual/templates/
dashboard/templates/
"""


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Locais onde o Django procura templates
        "DIRS": [
            BASE_DIR / "visual" / "templates",
            BASE_DIR / "dashboard" / "templates",
        ],
        # Encontra templates dentro dos apps automaticamente
        # EXEMPLO:
        # accounts/templates/accounts/login.html
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # EXEMPLO: mostra variáveis de debug no template
                "django.template.context_processors.debug",
                # EXEMPLO: permite acessar {{ request.user }} no HTML
                "django.template.context_processors.request",
                # EXEMPLO: {{ user }} no template
                "django.contrib.auth.context_processors.auth",
                # EXEMPLO: mensagens do tipo message.success/error
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# -----------------------------------------------------------
# 6. Static (CSS, JS, imagens)
# -----------------------------------------------------------

STATIC_URL = "/static/"

# EXEMPLO: onde seu Tailwind e assets ficam
STATICFILES_DIRS = [
    BASE_DIR / "visual" / "static",
]

# Pasta final onde tudo será coletado no deploy
STATIC_ROOT = BASE_DIR / "staticfiles"


# -----------------------------------------------------------
# 7. Django REST + JWT + django-allauth
# -----------------------------------------------------------

"""
DEFAULT_PERMISSION_CLASSES
Define quem pode acessar a API por padrão.

EXEMPLO:
IsAuthenticated → precisa estar logado
AllowAny → qualquer um pode acessar
"""
# ============================
# 🔐 AUTH / LOGIN FLOW
# ============================

# Onde o usuário vai depois de logar
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # EXEMPLO:
        # Authorization: Bearer <token>
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# EXEMPLO: /auth/registration/ usa esse serializer
REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "accounts.serializers.CustomRegisterSerializer",
}

# dj-rest-auth → habilitar JWT
REST_USE_JWT = True

# Configurações JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),  # token expira rápido
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # refresh dura mais
    "AUTH_HEADER_TYPES": ("Bearer",),  # Authorization: Bearer xxx
}


# -----------------------------------------------------------
# 8. Configurações Allauth
# -----------------------------------------------------------

# ✔ Email é obrigatório
ACCOUNT_EMAIL_REQUIRED = True

# ✔ username ainda é usado no Admin do Django
ACCOUNT_USERNAME_REQUIRED = True

# ✔ Login será feito por email
ACCOUNT_AUTHENTICATION_METHOD = "email"

# ✔ desnecessário em desenvolvimento, mas obrigatório em produção
ACCOUNT_EMAIL_VERIFICATION = "none"


# -----------------------------------------------------------
# 9. Internacionalização
# -----------------------------------------------------------

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"

# EXEMPLO: carrega traduções de pt-br
USE_I18N = True

# EXEMPLO: datetime será armazenado em UTC internamente
USE_TZ = True


# -----------------------------------------------------------
# 10. WSGI / ASGI
# -----------------------------------------------------------

# EXEMPLO:
# usado pelo Gunicorn em produção
WSGI_APPLICATION = "core.wsgi.application"

# EXEMPLO:
# usado pelo Uvicorn em tempo real (websockets)
ASGI_APPLICATION = "core.asgi.application"

# ==========================================================
# 🎨 JAZZMIN ADMIN SETTINGS — Versão Unificada e Profissional
# ==========================================================

# ==========================================================
# 🎨 JAZZMIN ADMIN SETTINGS — Versão Unificada e Profissional
# ==========================================================

JAZZMIN_SETTINGS = {
    # Branding principal
    "site_title": "ENEM Corrections Admin",
    "site_header": "Correções ENEM",
    "site_brand": "ENEM Pro",
    "welcome_sign": "Bem-vindo ao Painel Administrativo ENEM Pro",
    "copyright": "SoeiroTech © 2025",
    # Logo (opcional: coloque em visual/static/img/logo.png)
    # "site_logo": "img/logo.png",
    # "site_icon": "img/favicon.png",
    # Exibição e layout
    "show_sidebar": True,
    "navigation_expanded": True,
    "show_ui_builder": False,  # remove botão inútil do Jazzmin
    # Organização dos apps no menu lateral
    "order_with_respect_to": [
        "accounts",
        "profiles",
        "essays",
        "performance",
        "dashboard",
    ],
    # Links úteis no topo do admin
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Github", "url": "https://github.com/soeirotech"},
    ],
    # Ícones dos apps e modelos (Font Awesome)
    "icons": {
        "accounts.CustomUser": "fas fa-user",
        "profiles.StudentProfile": "fas fa-user-graduate",
        "profiles.TeacherProfile": "fas fa-chalkboard-teacher",
        "essays.Essay": "fas fa-file-alt",
        "essays.CompetenceScore": "fas fa-star",
        "performance": "fas fa-chart-line",
        "dashboard": "fas fa-tachometer-alt",
    },
    # Ícones padrão
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-file",
    # Cor principal do site (afeta barra superior)
    "site_color": "green",
}

# ==========================================================
# 🎨 Paleta de Cores Customizada — Tema Verde Profissional
# ==========================================================

JAZZMIN_COLORS = {
    "primary": "#0f766e",  # Verde esmeralda (Tailwind emerald-700)
    "secondary": "#064e3b",  # Verde profundo
    "accent": "#10b981",  # Verde claro moderno
    "dark": "#022c22",
    "light": "#f0fdfa",  # Off-white esverdeado
}

# ==========================================================
# 🖥️ UI Tweaks — Ajustes visuais finos
# ==========================================================

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",  # tema moderno claro
    "dark_mode_theme": "darkly",
    "navbar": "navbar-dark",
    "accent": "accent-green",  # combina com nossa paleta
    "navbar_small_text": False,
    "sidebar_small_text": False,
    "brand_small_text": False,
    "footer_small_text": False,
}
