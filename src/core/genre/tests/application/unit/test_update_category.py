from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.tests.application.integration.test_create_genre import movie_category


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)

@pytest.fixture
def mock_category_repository() -> CategoryRepository:
    return create_autospec(CategoryRepository)


class TestUpdateGenre:
    def test_update_genre_when_genre_does_not_exist_should_raise_genre_not_found_exception(self, mock_genre_repository, mock_category_repository):
        use_case = UpdateGenre(mock_genre_repository, mock_category_repository)
        mock_genre_repository.get_by_id.return_value = None

        with pytest.raises(GenreNotFound):
            use_case.execute(UpdateGenre.Input(id=uuid4(),name="Action", categories={uuid4()}, is_active=True))



    def test_update_genre_with_invalid_attributes_should_raise_invalid_exception(self, mock_genre_repository, mock_category_repository):
        movie_category = Category(name="Movie", description="Movie Description")
        mock_category_repository.list.return_value = [movie_category]

        genre = Genre(name="Action",
                      is_active=False,
                      categories={movie_category.id}
                      )
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(mock_genre_repository, mock_category_repository)

        with pytest.raises(InvalidGenre):
            use_case.execute(UpdateGenre.Input(id=genre.id, name="", categories=genre.categories, is_active=True))


    def test_update_genre_when_category_does_not_exist_should_raise_related_categories_not_found_exception(self, mock_genre_repository, mock_category_repository):
        genre = Genre(name="Action",
                      is_active=False,
                      categories={uuid4()}
                      )
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(mock_genre_repository, mock_category_repository)

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(UpdateGenre.Input(id=genre.id, name="Terror", categories={uuid4()}, is_active=True))

    def test_update_genre(self, mock_genre_repository, mock_category_repository):
        movie_category = Category(name="Movie", description="Movie Description")
        mock_category_repository.list.return_value = [movie_category]

        genre = Genre(
            name="Action",
            is_active=False,
            categories={movie_category.id}
        )
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(mock_genre_repository, mock_category_repository)

        input = UpdateGenre.Input(
            id=genre.id,
            name="Terror",
            is_active=True,
            categories=genre.categories
        )

        use_case.execute(input)

        mock_genre_repository.update(genre)

        assert genre.name == "Terror"
        assert genre.is_active is True
        assert genre.categories == {movie_category.id}