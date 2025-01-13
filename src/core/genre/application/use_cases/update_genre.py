from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.core.genre.application.exceptions import GenreNotFound, RelatedCategoriesNotFound, InvalidGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository





class UpdateGenre:

    def __init__(self, genre_repository: GenreRepository):
        self.genre_repository = genre_repository

    @dataclass
    class Input:
        id: UUID
        name: str
        is_active: bool
        category_ids: set[UUID]

    def execute(self, input: Input) -> None:
        genre = self.genre_repository.get_by_id(input.id)

        if genre is None:
            raise GenreNotFound(f"Genre with {input.id} not found")

        category_ids = {category_id for category_id in genre.categories}

        if not input.category_ids.issubset(category_ids):
            raise RelatedCategoriesNotFound(f"Categories not found: {input.category_ids - category_ids}")

        try:
            genre = Genre(
                id=genre.id,
                name=input.name,
                is_active=input.is_active,
                categories=input.category_ids
            )

        except ValueError as e:
            raise InvalidGenre(str(e))

        self.genre_repository.update(genre)

