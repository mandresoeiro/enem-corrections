from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    """Admin customizado para o modelo CustomUser.

    - Mostra o papel (role)
    - Permite filtrar por role
    - Usa email como identificador principal.
    """

    list_display = (
        "email",
        "username",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )
    list_filter = ("role", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = (
        ("Credenciais", {"fields": ("email", "username", "password")}),
        ("Informações pessoais", {"fields": ("first_name", "last_name")}),
        (
            "Papel e permissões",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "role", "password1", "password2"),
            },
        ),
    )
