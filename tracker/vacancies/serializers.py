from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Skills, City, FormsOfEmployment, WorkArrangements, Education
from users.serializers import CandidateSerializer
from vacancies.models import Vacancy


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"

    def create(self, validated_data):
        return Skills.objects.create(**validated_data)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

    def create(self, validated_data):
        return City.objects.create(**validated_data)


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"

    def create(self, validated_data):
        return Education.objects.create(**validated_data)


class WorkArrangementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkArrangements
        fields = "__all__"

    def create(self, validated_data):
        return WorkArrangements.objects.create(**validated_data)


class FormsOfEmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormsOfEmployment
        fields = "__all__"

    def create(self, validated_data):
        return FormsOfEmployment.objects.create(**validated_data)


class VacancySerializer(serializers.ModelSerializer):
    """Cериализатор вакансии."""

    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), default=1
    )
    job_title = serializers.CharField(max_length=200, label="Название вакансии")
    company_name = serializers.CharField(max_length=200, label="Название компании")
    min_salary = serializers.IntegerField(label="Зарплата от")
    max_salary = serializers.IntegerField(label="Зарплата до")
    description = serializers.CharField(label="Описание вакансии", required=False)
    experience_month = serializers.CharField(
        max_length=200, label="Опыт работы", required=False
    )
    pub_date = serializers.DateTimeField(read_only=True, label="Дата размещения")
    update_date = serializers.DateTimeField(read_only=True, label="Дата обновления")
    is_active = serializers.BooleanField(label="Активная вакансия")
    is_draft = serializers.BooleanField(label="Черновик")
    is_archived = serializers.BooleanField(label="Архивная")
    is_deleted = serializers.BooleanField(label="Удаленная")

    skills = SkillsSerializer(many=True, required=False)
    city = CitySerializer(required=False)
    form_of_employment = FormsOfEmploymentSerializer(required=False)
    work_arrangement = WorkArrangementsSerializer(many=True, required=False)
    education = EducationSerializer(required=False)

    class Meta:
        model = Vacancy
        fields = "__all__"

    def create(self, validated_data):
        skills_data = validated_data.pop("skills", [])
        city_data = validated_data.pop("city", None)
        form_of_employment_data = validated_data.pop("form_of_employment", None)
        work_arrangement_data = validated_data.pop("work_arrangement", [])
        education_data = validated_data.pop("education", None)

        # Создаем объект Vacancy без вложенных полей
        vacancy = Vacancy.objects.create(**validated_data)

        # Создаем связанные объекты, если они предоставлены в данных
        skills_serializer = SkillsSerializer(data=skills_data, many=True)
        if skills_serializer.is_valid():
            skills = [
                Skills.objects.get_or_create(name=skill_data["name"])[0]
                for skill_data in skills_data
            ]
            if skills:
                vacancy.skills.add(*skills)

        if city_data:
            city_serializer = CitySerializer(data=city_data)
            if city_serializer.is_valid():
                city_instance = city_serializer.save()
                vacancy.city = city_instance

        if form_of_employment_data:
            form_of_employment_serializer = FormsOfEmploymentSerializer(
                data=form_of_employment_data
            )
            if form_of_employment_serializer.is_valid():
                form_of_employment_instance = form_of_employment_serializer.save()
                vacancy.form_of_employment = form_of_employment_instance

        work_arrangement_serializer = WorkArrangementsSerializer(
            data=work_arrangement_data, many=True
        )
        if work_arrangement_serializer.is_valid():
            for work_arrangement_instance in work_arrangement_serializer.save():
                vacancy.work_arrangement.add(work_arrangement_instance)

        if education_data:
            education_serializer = EducationSerializer(data=education_data)
            if education_serializer.is_valid():
                education_instance = education_serializer.save()
                vacancy.education.set([education_instance])
        vacancy.save()
        return vacancy


class MatchCandidateSerializer(serializers.Serializer):
    candidate = CandidateSerializer()
    matching_skills = SkillsSerializer(many=True)
    matching_skills_count = serializers.IntegerField()
    matching_skills_percent = serializers.IntegerField()
