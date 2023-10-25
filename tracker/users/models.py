from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
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
    авторизация и взаимодействие с вакансиями и соискателями.
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
    Соискатель, загружается в базу данных на основе данных из карьерного трекера.
    """

    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="candidates",
        verbose_name="Город",
    )
    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name="Дата рождения"
    )
    status_from_kt = models.ForeignKey(
        Status_from_kt,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="candidates",
        verbose_name="Статус в карьерном треке",
    )
    form_of_employment = models.ManyToManyField(
        Forms_of_employment,
        related_name="candidate_employments",
        verbose_name="Тип занятости",
        blank=True,
    )
    work_arrangement = models.ManyToManyField(
        Work_arrangements,
        related_name="candidate_works",
        verbose_name="Формат работы",
        blank=True,
    )
    active = models.BooleanField(
        verbose_name="Активный пользователь",
        null=True,
        blank=True,
    )
    last_activity = models.DateTimeField(
        verbose_name="Был активен",
        null=True,
        blank=True,
    )
    experience_months = models.IntegerField(
        verbose_name="Опыт работы",
        null=True,
        blank=True,
    )
    education = models.ForeignKey(
        Education,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="candidates",
        verbose_name="Образование",
    )
    education_YP = models.ForeignKey(
        Education_YP,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="candidates",
        verbose_name="Курс в Яндекс Практикуме",
    )
    resume = models.FileField(
        upload_to="resumes/",
        verbose_name="Резюме",
        null=True,
        blank=True,
    )
    skills = models.ManyToManyField(
        Skills,
        related_name="candidate_skills",
        verbose_name="Навыки",
        blank=True,
    )
    mobile = models.CharField(
        max_length=16,
        verbose_name="Телефон",
        null=True,
        blank=True,
    )
    telegram = models.CharField(
        max_length=255,
        verbose_name="Телеграм",
        null=True,
        blank=True,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата размещения",
        null=True,
        blank=True,
    )

    groups = models.ManyToManyField(
        Group,
        related_name="candidate_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="candidate_user_permissions",
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Соискатель"
        verbose_name_plural = "Соискатели"


class Favorites(models.Model):
    """
    Модель-посредник для добавления кандидатов в избранное к рекрутерам.
    """

    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="favorited_by"
    )
    recruiter = models.ForeignKey(
        Recruiter, on_delete=models.CASCADE, related_name="favorites"
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"


class Ratings(models.Model):
    """Рейтинг, который рекрутер выставляет кандидату."""

    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="ratings"
    )
    recruiter = models.ForeignKey(
        Recruiter, on_delete=models.CASCADE, related_name="ratings"
    )
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Рейтинг должен быть не ниже 1"),
            MaxValueValidator(5, message="Рейтинг может быть не больше 5"),
        ]
    )

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинг"
