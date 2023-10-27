from rest_framework import serializers

from core.models import Skills
from users.serializers import CandidateSerializer
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


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"


class VacancySerializer(serializers.ModelSerializer):
    """Cериализатор вакансии."""

    user = serializers.StringRelatedField()
    skills = serializers.StringRelatedField(many=True)
    pub_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    city = serializers.StringRelatedField()
    form_of_employment = serializers.StringRelatedField()
    work_arrangement = serializers.StringRelatedField(many=True)

    # TODO Добавить валидацию

    class Meta:
        model = Vacancy
        exclude = ("is_active", "is_archived", "is_draft", "is_deleted")


class MatchCandidateSerializer(serializers.Serializer):
    candidate = CandidateSerializer()
    matching_skills = SkillSerializer(many=True)
    matching_skills_count = serializers.IntegerField()
    matching_skills_percent = serializers.IntegerField()
