from unittest.mock import create_autospec
from uuid import uuid4, UUID

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import RelatedCategoriesNotFound, InvalidGenre
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)

@pytest.fixture
def movie_category() -> Category:
    return Category(id=uuid4(),name="Movie")

@pytest.fixture
def series_category() -> Category:
    return Category(id=uuid4(),name="Series")

@pytest.fixture
def mock_category_repository_with_categories(movie_category, series_category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, series_category]
    return repository

@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository


class TestCreateGenre:
    def test_when_categories_do_not_exist_then_raise_related_categories_not_found(self, mock_empty_category_repository, mock_genre_repository):
        use_case = CreateGenre(genre_repository=mock_genre_repository, category_repository=mock_empty_category_repository)

        category_id = uuid4()
        input = CreateGenre.Input(name="Action", categories={category_id})

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input)

    def test_when_create_genre_is_invalid_then_raise_invalid_genre(self, movie_category, mock_category_repository_with_categories, mock_genre_repository):
        use_case = CreateGenre(genre_repository=mock_genre_repository, category_repository=mock_category_repository_with_categories)

        with pytest.raises(InvalidGenre, match="name cannot be empty"):
            use_case.execute(CreateGenre.Input(name="", categories={movie_category.id}))


    def test_when_created_genre_is_valid_and_categories_exist_then_save_genre(self, movie_category, series_category, mock_category_repository_with_categories, mock_genre_repository):
        use_case = CreateGenre(genre_repository=mock_genre_repository, category_repository=mock_category_repository_with_categories)

        categories = {movie_category.id, series_category.id}
        input = CreateGenre.Input(name="Action", categories=categories)

        use_case.execute(input)

        output = use_case.execute(input)

        assert isinstance(output.id, UUID)

        mock_genre_repository.save.assert_called_with(
            Genre(
                id=output.id,
                name="Action",
                is_active=True,
                categories={movie_category.id, series_category.id}
            )
        )

    def test_create_genre_without_categories(self, mock_genre_repository, mock_empty_category_repository):
        use_case = CreateGenre(genre_repository=mock_genre_repository, category_repository=mock_empty_category_repository)

        input = CreateGenre.Input(name="Action")

        use_case.execute(input)

        output = use_case.execute(input)

        assert isinstance(output.id, UUID)

        mock_genre_repository.save.assert_called_with(
            Genre(
                id=output.id,
                name="Action",
                is_active=True,
                categories=set()
            )
        )
