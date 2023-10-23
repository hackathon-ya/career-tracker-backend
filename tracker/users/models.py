from django.contrib.auth.models import AbstractUser
from django.db import models


class Recruiter(AbstractUser):
<<<<<<< HEAD
    """
    Рекрутер, основной пользователь, через которого осуществляется
    авторизация и взаимодействие с вакансиями и соискателями
    """

=======
>>>>>>> 5a6a717 (user models)
    company = models.CharField(max_length=200)
    company_inn = models.CharField(max_length=12)

    def __str__(self):
<<<<<<< HEAD
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Рекрутер"
        verbose_name_plural = "Рекрутеры"


class Candidate(AbstractUser):
    """
    Соискатель, загружается в базу данных на основе данных из карьерного трекера
    """

    city = models.ForeignKey(
        "City",
        on_delete=models.SET_NULL,
        related_name="candidates",
        verbose_name="Город",
    )
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    status_from_kt = models.ForeignKey(
        "Status_from_kt",
        on_delete=models.SET_NULL,
        related_name="candidates",
        verbose_name="Статус в карьерном треке",
=======
        return self.first_name + " " + self.last_name


class Candidate(AbstractUser):
    city = models.ForeignKey(
        "City", on_delete=models.SET_NULL, related_name="candidates", verbose_name="Город"
    )
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    status_from_kt = models.ForeignKey(
        "Status_from_kt", on_delete=models.SET_NULL, related_name="candidates", verbose_name="Статус в карьерном треке"
>>>>>>> 5a6a717 (user models)
    )
    form_of_employment = models.ManyToManyField(
        "Forms_of_employment", related_name="candidates", verbose_name="Тип занятости"
    )
    work_arrangement = models.ManyToManyField(
        "Work_arrangements", related_name="candidates", verbose_name="Формат работы"
    )
    active = models.BooleanField(verbose_name="Активный пользователь")
    last_activity = models.DateTimeField(verbose_name="Был активен")
    experience_months = models.IntegerField(verbose_name="Опыт работы")
    education = models.ForeignKey(
<<<<<<< HEAD
        "Education",
        on_delete=models.SET_NULL,
        related_name="candidates",
        verbose_name="Образование",
    )
    education_YP = models.ForeignKey(
        "Education_YP",
        on_delete=models.SET_NULL,
        related_name="candidates",
        verbose_name="Курс в Яндекс Практикуме",
    )
    resume = models.FileField(upload_to="resumes/", verbose_name="Резюме")
    skills = models.ManyToManyField(
        "Skills", related_name="candidates", verbose_name="Навыки"
    )
=======
        "Education", on_delete=models.SET_NULL, related_name="candidates", verbose_name="Образование"
    )
    education_YP = models.ForeignKey(
        "Education_YP", on_delete=models.SET_NULL, related_name="candidates", verbose_name="Курс в Яндекс Практикуме"
    )
    resume = models.FileField(upload_to="resumes/", verbose_name="Резюме")
    skills = models.ManyToManyField("Skills", related_name="candidates", verbose_name="Навыки")
>>>>>>> 5a6a717 (user models)
    mobile = models.CharField(max_length=16, verbose_name="Телефон")
    telegram = models.CharField(verbose_name="Телеграм")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата размещения")

    def __str__(self):
<<<<<<< HEAD
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Соискатель"
        verbose_name_plural = "Соискатели"


class Favorites(models.Model):
    """
    Модель-посредник для добавление кандидатов в избранное к рекрутерам
    """

=======
        return self.first_name + " " + self.last_name


class Favorites(models.Model):
>>>>>>> 5a6a717 (user models)
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="favorited_by"
    )
    recruiter = models.ForeignKey(
        Recruiter, on_delete=models.CASCADE, related_name="favorites"
    )
