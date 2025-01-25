from django.contrib import admin
from django.urls import path


from rest_framework.routers import DefaultRouter

from src.django_project.category.views import CategoryViewSet
from src.django_project.genre.views import GenreViewSet

router = DefaultRouter()
router.register(r"api/categories", CategoryViewSet, basename="category")
router.register(r"api/genres", GenreViewSet, basename="genre")

urlpatterns = [
    path("admin/", admin.site.urls),
] + router.urls
