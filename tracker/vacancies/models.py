from django.contrib.auth import get_user_model
from django.db import models
from core.models import City, Skills, FormsOfEmployment, WorkArrangements, Education


class Vacancy(models.Model):
    """Вакансия."""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="Рекрутер",
    )

    job_title = models.CharField(max_length=200, verbose_name="Название вакансии")
    company_name = models.CharField(max_length=200, verbose_name="Название компании")
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Город"
    )
    min_salary = models.IntegerField(verbose_name="Зарплата от")
    max_salary = models.IntegerField(verbose_name="Зарплата до")
    skills = models.ManyToManyField(
        Skills, related_name="vacancies", verbose_name="Навыки", blank=True
    )
    description = models.TextField(verbose_name="Описание вакансии")
    experience_month = models.CharField(
        max_length=200, verbose_name="Опыт работы", blank=True, null=True
    )
    form_of_employment = models.ForeignKey(
        FormsOfEmployment,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="vacancies",
        verbose_name="Тип занятости",
    )
    work_arrangement = models.ManyToManyField(
        WorkArrangements,
        related_name="vacancies",
        verbose_name="Формат работы",
        blank=True,
    )
    education = models.ManyToManyField(
        Education, related_name="vacancies", verbose_name="Образование", blank=True
    )

    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата размещения")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    is_active = models.BooleanField(verbose_name="Активная вакансия")
    is_draft = models.BooleanField(verbose_name="Черновик")
    is_archived = models.BooleanField(verbose_name="Архивная")
    is_deleted = models.BooleanField(verbose_name="Удаленная")

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.job_title

    def delete(self, using=None, keep_parents=False):
        """Мягкое удаление."""
        self.is_active = False
        self.is_draft = False
        self.is_archived = True
        self.is_deleted = True
        self.save(
            using=using,
            update_fields=["is_deleted", "is_active", "is_draft", "is_archived"],
        )
