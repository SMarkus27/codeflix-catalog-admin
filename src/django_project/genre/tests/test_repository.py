import pytest

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category.repository import DjangoORMCategoryRepository
from src.django_project.genre.repository import DjangoORMGenreRepository
from src.django_project.genre.models import Genre as GenreModel


@pytest.mark.django_db
class TestSave:
    def test_saves_genre(self):
        genre = Genre(name="Action")
        genre_repository = DjangoORMGenreRepository()

        assert GenreModel.objects.count() == 0
        genre_repository.save(genre)

        assert GenreModel.objects.count() == 1
        genre_model = GenreModel.objects.first()

        assert genre_model.name == "Action"
        assert genre_model.id == genre.id
        assert genre_model.is_active is True

    def test_saves_genre_with_categories(self):
        genre_repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        category = Category(name="Movie")
        category_repository.save(category)

        genre = Genre(name="Action", categories={category.id})

        assert GenreModel.objects.count() == 0
        genre_repository.save(genre)

        assert GenreModel.objects.count() == 1

        genre_model = GenreModel.objects.get(id=genre.id)
        related_categories = genre_model.categories.get()

        assert related_categories.name == "Movie"
        assert related_categories.id == category.id

