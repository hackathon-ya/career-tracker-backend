from django.urls import include, path
from rest_framework import routers

from users.views import (
    CandidateViewSet,
)

router = routers.DefaultRouter()
router.register(r"candidates", CandidateViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
