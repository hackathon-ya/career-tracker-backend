from django.urls import include, path
from rest_framework import routers

from vacancies.views import VacancyViewSet

router = routers.DefaultRouter()
router.register(r"vacancies", VacancyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
