from django.urls import include, path
from rest_framework import routers

from vacancies.views import MatchCandidateViewSet, VacancyViewSet

app_name = "vacancies"

router = routers.DefaultRouter()
router.register(r"vacancies", VacancyViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "vacancies/<int:pk>/candidates/", MatchCandidateViewSet.as_view(), name="search"
    ),
]
