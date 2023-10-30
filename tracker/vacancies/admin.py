from django.contrib import admin

from .models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        "job_title",
        "experience_month",
        "is_active",
        "is_draft",
        "is_archived",
        "is_deleted",
    )
    search_fields = ("job_title",)
    list_filter = ("is_active", "is_draft", "is_archived", "is_deleted")
    empty_value_display = "-пусто-"
