from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository():
    return create_autospec(GenreRepository)



class TestDeleteGenre:

    def test_delete_genre(self, mock_genre_repository):
        genre = Genre(name="Action")
        mock_genre_repository.get_by_id.return_value = genre

        use_case = DeleteGenre(mock_genre_repository)
        use_case.execute(DeleteGenre.Input(id=genre.id))

        mock_genre_repository.get_by_id.assert_called_once_with(genre.id)


    def test_delete_genre_not_exist_then_raise_found_exception(self, mock_genre_repository):
        mock_genre_repository.get_by_id.return_value = None

        use_case = DeleteGenre(mock_genre_repository)
        with pytest.raises(GenreNotFound, match="Genre with .* not found"):
            use_case.execute(DeleteGenre.Input(uuid4()))

        mock_genre_repository.delete.assert_not_called()
