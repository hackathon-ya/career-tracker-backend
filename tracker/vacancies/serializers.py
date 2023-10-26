from rest_framework import serializers

from vacancies.models import Vacancy


class VacancyReadSerializer(serializers.ModelSerializer):
    """Сериализатор вакансии."""

    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    city = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )
    form_of_employment = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )
    work_arrangement = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = Vacancy
        fields = (
            "id",
            "job_title",
            "company_name",
            "city",
            "min_salary",
            "max_salary",
            "skills",
            "description",
            "experience_month",
            "form_of_employment",
            "work_arrangement",
            "pub_date",
            "update_date",
            "is_active",
            "is_draft",
            "is_archived",
            "is_deleted",
        )


class VacancyWriteSerializer(serializers.ModelSerializer):
    """Cериализатор вакансии."""

    # TODO Добавить валидацию

    class Meta:
        model = Vacancy
        fields = "__all__"
