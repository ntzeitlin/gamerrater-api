from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from raterapi.views import (
    ReviewViewSet,
    GameViewSet,
    CategoryViewSet,
    register_user,
    login_user,
    PictureViewSet,
)

router = DefaultRouter(trailing_slash=False)

router.register(r"games", GameViewSet, "game")
router.register(r"categories", CategoryViewSet, "category")
router.register(r"reviews", ReviewViewSet, "review")
router.register(r"pictures", PictureViewSet, "picture")

urlpatterns = [
    path("", include(router.urls)),
    path("login", login_user),
    path("register", register_user),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
