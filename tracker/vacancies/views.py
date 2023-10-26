from rest_framework import mixins, status, viewsets
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

        # Retrieve all candidates
        candidates = Candidate.objects.all()

        # Create a list to store data for each candidate
        data = []

        for candidate in candidates:
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
