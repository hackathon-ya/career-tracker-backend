from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from core.models import (
    City,
    Status_from_kt,
    Forms_of_employment,
    Work_arrangements,
    Education,
    Education_YP,
    Skills,
)


class Recruiter(AbstractUser):
    """
    Рекрутер, основной пользователь, через которого осуществляется
    авторизация и взаимодействие с вакансиями и соискателями
    """

    company = models.CharField(max_length=200)
    company_inn = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Рекрутер"
        verbose_name_plural = "Рекрутеры"


class Candidate(AbstractUser):
    """
    Соискатель, загружается в базу данных на основе данных из карьерного трекера
    """

    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        related_name="candidates",
        verbose_name="Город",
    )
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    status_from_kt = models.ForeignKey(
        Status_from_kt,
        on_delete=models.SET_NULL,
        null=True,
        related_name="candidates",
        verbose_name="Статус в карьерном треке",
    )
    form_of_employment = models.ManyToManyField(
        Forms_of_employment, related_name="candidate_employments", verbose_name="Тип занятости"
    )
    work_arrangement = models.ManyToManyField(
        Work_arrangements, related_name="candidate_works", verbose_name="Формат работы"
    )
    active = models.BooleanField(verbose_name="Активный пользователь")
    last_activity = models.DateTimeField(verbose_name="Был активен")
    experience_months = models.IntegerField(verbose_name="Опыт работы")
    education = models.ForeignKey(
        Education,
        on_delete=models.SET_NULL,
        null=True,
        related_name="candidates",
        verbose_name="Образование",
    )
    education_YP = models.ForeignKey(
        Education_YP,
        on_delete=models.SET_NULL,
        null=True,
        related_name="candidates",
        verbose_name="Курс в Яндекс Практикуме",
    )
    resume = models.FileField(upload_to="resumes/", verbose_name="Резюме")
    skills = models.ManyToManyField(
        Skills, related_name="candidate_skills", verbose_name="Навыки"
    )
    mobile = models.CharField(max_length=16, verbose_name="Телефон")
    telegram = models.CharField(max_length=255, verbose_name="Телеграм")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата размещения")

    groups = models.ManyToManyField(
        Group, related_name='recruiter_groups', verbose_name="Группы"
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name='recruiter_user_permissions', verbose_name="Права пользователя"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Соискатель"
        verbose_name_plural = "Соискатели"


class Favorites(models.Model):
    """
    Модель-посредник для добавления кандидатов в избранное к рекрутерам
    """

    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="favorited_by"
    )
    recruiter = models.ForeignKey(
        Recruiter, on_delete=models.CASCADE, related_name="favorites"
    )
    groups = models.ManyToManyField(
        Group, related_name='candidate_groups', verbose_name="Группы"
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name='candidate_user_permissions', verbose_name="Права пользователя"
    )
