from dataclasses import field, dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import RelatedCategoriesNotFound, InvalidGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class CreateGenre:
    def __init__(self, genre_repository: GenreRepository, category_repository: CategoryRepository):
        self.genre_repository = genre_repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        name: str
        is_active: bool = True
        category_ids: set[UUID] = field(default_factory=set)


    @dataclass
    class Output:
        id: UUID


    def execute(self,  input: Input):
        category_ids = {category.id for category in self.category_repository.list()}

        if not input.category_ids.issubset(category_ids):
            raise RelatedCategoriesNotFound(f"Categories not found: {input.category_ids - category_ids}")

        try:
            genre = Genre(
                name=input.name,
                is_active=input.is_active,
                categories=input.category_ids
            )

        except ValueError as e:
            raise InvalidGenre(str(e))

        self.genre_repository.save(genre)
        return self.Output(id=genre.id)
