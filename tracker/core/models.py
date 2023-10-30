from django.db import models


class City(models.Model):
    """Город."""

    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class StatusFromKt(models.Model):
    """Статус в карьерном треке."""

    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус в карьерном треке"
        verbose_name_plural = "Статусы в карьерном треке"


class FormsOfEmployment(models.Model):
    """Тип занятости."""

    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип занятости"
        verbose_name_plural = "Типы занятости"


class WorkArrangements(models.Model):
    """Формат работы."""

    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Формат работы"
        verbose_name_plural = "Форматы работы"


class Education(models.Model):
    """Образование."""

    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Образование"
        verbose_name_plural = "Образования"


class EducationYp(models.Model):
    """Курс в Яндекс Практикуме."""

    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс в Яндекс Практикуме"
        verbose_name_plural = "Курсы в Яндекс Практикуме"


class Skills(models.Model):
    """Навыки."""

    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Навыки"
        verbose_name_plural = "Навыки"
