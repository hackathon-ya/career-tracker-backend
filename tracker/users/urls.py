from django.urls import include, path
from rest_framework import routers

from users.views import (
    APIAddFavorite,
    CandidateViewSet,
    FavoritesViewSet,
)

app_name = 'users'

router = routers.DefaultRouter()
router.register(r"candidates", CandidateViewSet)
router.register(r"favorites", FavoritesViewSet)


urlpatterns = [
    path("candidates/<int:pk>/favorite/", APIAddFavorite.as_view()),
    path("", include(router.urls)),
]
