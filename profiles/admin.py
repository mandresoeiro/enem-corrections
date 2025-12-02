from django.contrib import admin
from .models import StudentProfile, TeacherProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "grade", "total_essays", "created_at")
    search_fields = ("user__email", "course")


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "subjects", "total_corrections", "created_at")
    search_fields = ("user__email",)
