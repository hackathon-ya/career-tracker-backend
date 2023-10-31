from django.contrib import admin

from .models import (
    City,
    Education,
    EducationYp,
    FormsOfEmployment,
    Skills,
    StatusFromKt,
    WorkArrangements,
)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(StatusFromKt)
class Status_from_ktAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(FormsOfEmployment)
class Forms_of_employmentAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(WorkArrangements)
class Work_arrangementsAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(EducationYp)
class EEducation_YPAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ("name",)
