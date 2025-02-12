from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.use_cases.list_genre import ListGenre, GenreOutput, ListGenreRequest, ListGenreResponse, \
    ListOutputMeta
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestListGenre:
    def test_list_genres_with_associated_categories(self):
        category_repository = InMemoryCategoryRepository()

        movie_category = Category(name="Movie")
        category_repository.save(movie_category)

        series_category = Category(name="Series")
        category_repository.save(series_category)

        genre_repository = InMemoryGenreRepository()
        genre = Genre(
            name="Action",
            categories={movie_category.id, series_category.id}
        )
        genre_repository.save(genre)

        use_case = ListGenre(genre_repository)

        input = ListGenreRequest()
        output = use_case.execute(input)

        assert len(output.data) == 1
        assert output == ListGenreResponse(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=True,
                    categories={series_category.id, movie_category.id}
                )
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=1
            )
        )

    def test_list_genres_without_associated_categories(self):
        genre_repository = InMemoryGenreRepository()
        genre = Genre(name="Action")
        genre_repository.save(genre)

        use_case = ListGenre(genre_repository)

        input = ListGenreRequest()
        output = use_case.execute(input)

        assert len(output.data) == 1
        assert output == ListGenreResponse(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=True,
                    categories=set()
                )
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=1
            )
        )