from rest_framework import mixins, viewsets

from vacancies.models import Vacancy
from vacancies.serializers import VacancyReadSerializer


class ListRetrieveViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    pass


class VacancyViewSet(ListRetrieveViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyReadSerializer
    # TODO Добавить фильтр
