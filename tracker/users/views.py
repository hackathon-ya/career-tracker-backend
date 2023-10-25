from rest_framework import filters, mixins, viewsets

from users.models import Candidate
from users.serializers import CandidateSerializer


class ListRetrieveViewset(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    pass


class CandidateViewSet(ListRetrieveViewset):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
