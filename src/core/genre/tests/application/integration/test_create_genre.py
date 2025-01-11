from uuid import uuid4, UUID

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.exceptions import RelatedCategoriesNotFound
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(id=uuid4(),name="Movie")

@pytest.fixture
def series_category() -> Category:
    return Category(id=uuid4(),name="Series")

@pytest.fixture
def category_repository(movie_category, series_category) -> CategoryRepository:
    return InMemoryCategoryRepository(
        categories=[movie_category,series_category]
    )

class TestCreateGenre:
    def test_create_genre_with_associated_categories(self, movie_category, series_category, category_repository):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(genre_repository=genre_repository, category_repository=category_repository)

        input = CreateGenre.Input(
            name="Action",
            category_ids={movie_category.id, series_category.id}
        )

        output = use_case.execute(input)

        assert isinstance(output.id, UUID)

        saved_genre = genre_repository.get_by_id(output.id)

        assert saved_genre.name == "Action"
        assert saved_genre.categories == {movie_category.id, series_category.id}
        assert saved_genre.is_active is True

    def test_create_genre_with_inexistent_categories_raise_an_error(self, category_repository):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(genre_repository=genre_repository, category_repository=category_repository)

        input = CreateGenre.Input(
            name="Action",
            category_ids={uuid4()}
        )

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input)

    def test_create_genre_without_categories(self, category_repository):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(genre_repository=genre_repository, category_repository=category_repository)

        input = CreateGenre.Input(name="Action")

        output = use_case.execute(input)

        assert isinstance(output.id, UUID)

        assert isinstance(output.id, UUID)

        saved_genre = genre_repository.get_by_id(output.id)

        assert saved_genre.name == "Action"
        assert saved_genre.categories == set()
        assert saved_genre.is_active is True