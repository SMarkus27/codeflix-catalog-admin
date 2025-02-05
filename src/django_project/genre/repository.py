from uuid import UUID

from django.db import transaction

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre.models import Genre as GenreModel

class DjangoORMGenreRepository(GenreRepository):
    def save(self, genre: Genre) -> None:

        with transaction.atomic():
            genre_model = GenreModel.objects.create(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active
            )

            genre_model.categories.set(genre.categories)


    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            genre_model = GenreModel.objects.get(id=id)
        except GenreModel.DoesNotExist:
            return None

        return Genre(
            id=genre_model.id,
            name=genre_model.name,
            is_active=genre_model.is_active,
            categories={category.id for category in genre_model.categories.all()}
        )

    def list(self) -> list[Genre]:
        return [
            Genre(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories={category.id for category in genre.categories.all()}
            )
            for genre in GenreModel.objects.all()
        ]

    def delete(self, id: UUID) -> None:
        GenreModel.objects.filter(id=id).delete()

    def update(self, genre) -> None:
        try:
            genre_model = GenreModel.objects.get(id=genre.id)
        except GenreModel.DoesNotExist:
            return None

        with transaction.atomic():
            GenreModel.objects.filter(id=genre.id).update(
                name=genre.name,
                is_active=genre.is_active
            )

            genre_model.categories.set(genre.categories)
