from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

from core.filters import CandidateFilter
from users.models import Candidate
from users.serializers import CandidateSerializer


class ListRetrieveViewset(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    pass


class CandidateViewSet(ListRetrieveViewset):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CandidateFilter
    filterset_fields = {
        "city": ["exact"],  # Filtering by exact match
        "education": ["exact"],
        "education_YP": ["exact"],
        "status_from_kt": ["exact"],
    }
