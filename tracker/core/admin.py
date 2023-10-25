from django.contrib import admin

from .models import (
    City,
    Status_from_kt,
    Forms_of_employment,
    Work_arrangements,
    Education,
    Education_YP,
    Skills,
)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Status_from_kt)
class Status_from_ktAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Forms_of_employment)
class Forms_of_employmentAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Work_arrangements)
class Work_arrangementsAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Education_YP)
class EEducation_YPAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ("name",)
