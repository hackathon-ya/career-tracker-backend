from django.urls import include, path
from rest_framework import routers

from vacancies.views import MatchCandidateViewSet, VacancyViewSet

router = routers.DefaultRouter()
router.register(r"vacancies", VacancyViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "vacancies/<int:pk>/candidates/", MatchCandidateViewSet.as_view({"get": "list"})
    ),
]
