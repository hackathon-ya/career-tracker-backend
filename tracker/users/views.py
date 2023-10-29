from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from core.filters import CandidateFilter
from users.models import Candidate, Favorites
from users.serializers import CandidateSerializer


recruiter = get_user_model().objects.get(id=1)


class ListRetrieveViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    pass


class CandidateViewSet(ListRetrieveViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_class = CandidateFilter
    search_fields = ("^job_title",)


class APIAddFavorite(APIView):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        candidate = get_object_or_404(Candidate, pk=pk)

        if not Favorites.objects.filter(
            candidate=candidate, recruiter=recruiter
        ).exists():
            Favorites.objects.create(candidate=candidate, recruiter=recruiter)

        serializer = CandidateSerializer(candidate, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        candidate = get_object_or_404(Candidate, pk=pk)

        if Favorites.objects.filter(candidate=candidate, recruiter=recruiter).exists():
            Favorites.objects.get(candidate=candidate, recruiter=recruiter).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoritesViewSet(ListRetrieveViewSet):
    queryset = Candidate.objects.filter(favorited_by__recruiter=recruiter)
    serializer_class = CandidateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CandidateFilter
