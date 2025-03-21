from django.urls import include, path
from rest_framework.routers import DefaultRouter
from raterapi.views import (
    UserViewSet,
    GameViewSet,
    CategoryViewSet,
    register_user,
    login_user,
)

router = DefaultRouter(trailing_slash=False)

router.register(r"games", GameViewSet, "game")
router.register(r"categories", CategoryViewSet, "category")

urlpatterns = [
    path("", include(router.urls)),
    path("login", login_user),
    path("register", register_user),
]
