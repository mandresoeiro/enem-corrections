"""
URL principal do projeto ENEM Corrections.

Organização:
1) Admin (Jazzmin)
2) Autenticação HTML (login visual personalizado)
3) Autenticação REST (dj-rest-auth + allauth)
4) Dashboard (Django Templates)
5) API REST v1 — Accounts, Profiles, Essays, Performance
6) Healthcheck
7) Static & Media (modo DEV)
8) Preparado para API v2
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


# ==========================================================
# HEALTHCHECK — útil em Docker, Railway, Render e CI/CD
# ==========================================================


def healthcheck(_request):
    return JsonResponse(
        {
            "status": "ok",
            "app": "ENEM Corrections API",
            "debug": settings.DEBUG,
        }
    )


# ==========================================================
# URLS PRINCIPAIS
# ==========================================================

urlpatterns = [
    # ------------------------------------------------------
    # 1. Django Admin (Jazzmin)
    # ------------------------------------------------------
    path("admin/", admin.site.urls),
    # ------------------------------------------------------
    # 2. LOGIN HTML PERSONALIZADO
    # ------------------------------------------------------
    # 🔥 ESSENCIAL:
    # Essa rota substitui o login padrão do django.
    # O dashboard, quando exige LoginRequiredMixin,
    # redireciona para LOGIN_URL = "/accounts/login/".
    #
    # Portanto, essa rota DEVE EXISTIR.
    path(
        "accounts/login/",
        TemplateView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("accounts/", include("accounts.urls")),
    # ------------------------------------------------------
    # 3. Autenticação REST (JSON) — dj-rest-auth / allauth
    # ------------------------------------------------------
    # Login via API, logout, refresh, user-details
    path("auth/", include("dj_rest_auth.urls")),
    # Registro do usuário
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    # ------------------------------------------------------
    # 4. Dashboard HTML
    # ------------------------------------------------------
    # Interface visual (classe protegida por login)
    path("", include("dashboard.urls")),
    # ------------------------------------------------------
    # 5. API REST — versão 1
    # ------------------------------------------------------
    path("api/accounts/", include("accounts.urls")),
    path("api/profiles/", include("profiles.urls")),
    path("api/essays/", include("essays.urls")),
    path("api/performance/", include("performance.urls")),
    # ------------------------------------------------------
    # 6. Healthcheck
    # ------------------------------------------------------
    path("health/", healthcheck, name="healthcheck"),
    # ------------------------------------------------------
    # 7. API FUTURA v2 (placeholder)
    # ------------------------------------------------------
    # path("api/v2/", include("api_v2.urls")),
]


# ==========================================================
# 8. Static e Media em modo DEV
# ==========================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
