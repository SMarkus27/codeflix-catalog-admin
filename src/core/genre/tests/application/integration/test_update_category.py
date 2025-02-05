from uuid import uuid4

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestUpdateGenre:

    def test_can_update_genre(self):
        category_repository = InMemoryCategoryRepository()

        movie_category = Category(name="Movie")
        category_repository.save(movie_category)

        serie_category = Category(name="Serie")
        category_repository.save(serie_category)


        genre_repository = InMemoryGenreRepository()

        genre = Genre(
            name="Action",
            categories={movie_category.id, serie_category.id},
            is_active=False
      )

        genre_repository.save(genre)

        use_case = UpdateGenre(genre_repository, category_repository)

        input = UpdateGenre.Input(
            id=genre.id,
            name="Terror",
            is_active=True,
            categories={movie_category.id}
        )

        use_case.execute(input)

        updated_genre = genre_repository.get_by_id(genre.id)

        assert updated_genre.name == "Terror"
        assert updated_genre.is_active is True
        assert updated_genre.categories == {movie_category.id}