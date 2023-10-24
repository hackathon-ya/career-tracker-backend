from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Recruiter, Candidate


@admin.register(Recruiter)
class RecruiterAdmin(UserAdmin):
    list_display = (
        "company",
        "company_inn",
        "first_name",
        "last_name",
        "email",
    )


@admin.register(Candidate)
class CandidateAdmin(UserAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "date_of_birth",
        "active",
    )
