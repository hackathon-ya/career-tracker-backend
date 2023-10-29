from django.db.models import Q
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView


from core.models import City, FormsOfEmployment, WorkArrangements, Skills
from users.models import Candidate
from vacancies.models import Vacancy
from vacancies.serializers import (
    MatchCandidateSerializer,
    VacancySerializer,
    SkillsSerializer,
)


class ListRetrieveViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pass


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

    def perform_create(self, serializer):
        # Получение или создание объектов City, FormsOfEmployment, WorkArrangements
        city, _ = City.objects.get_or_create(name=self.request.data.get("city"))
        skills = (
            Skills.objects.get_or_create(name=name)
            for name in self.request.data.get("skills", [])
        )
        form_of_employment, _ = FormsOfEmployment.objects.get_or_create(
            name=self.request.data.get("form_of_employment")
        )
        work_arrangements = (
            WorkArrangements.objects.get_or_create(name=name)
            for name in self.request.data.get("work_arrangement", [])
        )

        # Сохранение объектов вакансии
        instance = serializer.save(city=city, form_of_employment=form_of_employment)
        instance.work_arrangement.set(work_arrangements)
        instance.skills.set(skills)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class MatchCandidateViewSet(APIView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        try:
            # Retrieve the vacancy object based on the vacancy_id from the URL
            vacancy = Vacancy.objects.get(pk=pk)
        except Vacancy.DoesNotExist:
            return Response(
                {"error": "Vacancy not found"}, status=status.HTTP_404_NOT_FOUND
            )

        base_filter = Q()
        if vacancy.form_of_employment is not None:
            base_filter &= Q(form_of_employment=vacancy.form_of_employment)
        if vacancy.city is not None:
            base_filter &= Q(city=vacancy.city)
        if vacancy.experience_month is not None:
            base_filter &= Q(experience_months__gte=vacancy.experience_month)
        if vacancy.work_arrangement.count() != 0:
            base_filter &= Q(work_arrangement__in=vacancy.work_arrangement.all())

        filtered_candidates = Candidate.objects.filter(base_filter)

        # Create a list to store data for each candidate
        data = []

        for candidate in filtered_candidates:
            candidate_skills = candidate.skills.all()
            vacancy_skills = vacancy.skills.all()
            matching_skills = candidate_skills.filter(
                id__in=vacancy_skills.values_list("id", flat=True)
            )
            if vacancy_skills.count() > 0:
                percent = (matching_skills.count() / vacancy_skills.count()) * 100
            else:
                percent = 0

            matching_skills_data = SkillsSerializer(matching_skills, many=True).data

            data.append(
                {
                    "candidate": candidate,
                    "matching_skills": matching_skills_data,
                    "matching_skills_count": matching_skills.count(),
                    "matching_skills_percent": round(percent),
                }
            )

        # Sort the data by decreasing matching_skills_percent
        data.sort(key=lambda x: x["matching_skills_percent"], reverse=True)

        # Serialize the data using the CandidateMatchSerializer
        serializer = MatchCandidateSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
