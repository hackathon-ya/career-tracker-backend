from django.contrib import admin

from .models import Recruiter, Candidate, Favorites, Ratings


@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "company",
        "company_inn",
        "first_name",
        "last_name",
        "email",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email")}),
        ("Company", {"fields": ("company", "company_inn")}),
    )
    search_fields = ("username",)
    empty_value_display = "-пусто-"


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "date_of_birth",
        "active",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "email", "date_of_birth", "city")},
        ),
        ("Status", {"fields": ("status_from_kt", "active", "last_activity")}),
        ("Employment", {"fields": ("form_of_employment", "work_arrangement")}),
        ("Education", {"fields": ("education", "education_YP")}),
        ("Skills", {"fields": ("skills",)}),
        ("Contact Info", {"fields": ("mobile", "telegram")}),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
    )
    search_fields = (
        "first_name",
        "last_name",
    )
    list_filter = (
        "active",
        "form_of_employment",
        "work_arrangement",
        "education",
        "education_YP",
        "skills",
    )
    empty_value_display = "-пусто-"


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ("candidate", "recruiter")


@admin.register(Ratings)
class RatingsAdmin(admin.ModelAdmin):
    list_display = ("candidate", "recruiter", "rating")
