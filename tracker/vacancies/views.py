from django.db.models import Q
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from users.models import Candidate
from vacancies.models import Vacancy
from vacancies.serializers import (
    MatchCandidateSerializer,
    VacancySerializer,
    SkillSerializer,
)


class ListRetrieveViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pass


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("^job_title",)
    # TODO Добавить фильтр


class MatchCandidateViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
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
            percent = (matching_skills.count() / vacancy_skills.count()) * 100

            matching_skills_data = SkillSerializer(matching_skills, many=True).data

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
