from uuid import uuid4

import pytest

from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestDeleteGenre:

    def test_delete_genre(self):
        genre = Genre(name="Action")
        genre_repository = InMemoryGenreRepository([genre])

        use_case = DeleteGenre(genre_repository)

        input = DeleteGenre.Input(id=genre.id)

        assert genre_repository.get_by_id(genre.id) is not None

        use_case.execute(input)

        assert genre_repository.get_by_id(genre.id) is None


    def test_delete_genre_not_exist_then_raise_found_exception(self):
        genre_repository = InMemoryGenreRepository([])

        use_case = DeleteGenre(genre_repository)
        with pytest.raises(GenreNotFound, match="Genre with .* not found"):
            use_case.execute(DeleteGenre.Input(uuid4()))

