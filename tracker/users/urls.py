from django.urls import include, path
from rest_framework import routers

from users.views import (
    APIAddFavorite,
    CandidateViewSet,
    FavoritesViewSet,
)

app_name = "users"

router = routers.DefaultRouter()
router.register(r"candidates", CandidateViewSet, basename="candidates")
router.register(r"favorites", FavoritesViewSet, basename="favorites")


urlpatterns = [
    path("candidates/<int:pk>/favorite/", APIAddFavorite.as_view(), name="favorite"),
    path("", include(router.urls)),
]
