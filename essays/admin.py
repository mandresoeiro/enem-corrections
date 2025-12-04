from django.contrib import admin
from .models import Essay

@admin.register(Essay)
class EssayAdmin(admin.ModelAdmin):
    list_display = ("title", "student", "status", "created_at")
    search_fields = ("title", "student__email")
    list_filter = ("status", "created_at")
