from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.list_genre import ListGenre, GenreOutput
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


class TestListGenre:
    def test_list_genres_with_associated_categories(self, movie_category, series_category, mock_genre_repository):
        category_ids = {movie_category.id, series_category.id}
        genre = Genre(name="Action", categories=category_ids)

        mock_genre_repository.list.return_value = [genre]

        use_case = ListGenre(mock_genre_repository)

        output = use_case.execute(ListGenre.Input())
        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=True,
                    categories={movie_category.id, series_category.id}
                )
            ]
        )

    def test_list_genres_without_associated_categories(self, mock_genre_repository):
        genre = Genre(name="Action")
        mock_genre_repository.list.return_value = [genre]

        use_case = ListGenre(mock_genre_repository)

        output = use_case.execute(ListGenre.Input())
        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=True,
                    categories=set()
                )
            ]
        )