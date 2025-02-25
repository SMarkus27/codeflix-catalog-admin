from dataclasses import dataclass, field
from uuid import UUID

from src.config import DEFAULT_PER_PAGE_SIZE
from src.core._shared.list import ListOutputMeta, ListRequest
from src.core.genre.domain.genre_repository import GenreRepository

@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]

@dataclass
class ListGenreResponse:
    data: list[GenreOutput]
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)

class ListGenre:
    def __init__(self, genre_repository: GenreRepository):
        self.genre_repository = genre_repository

    def execute(self, request: ListRequest) -> ListGenreResponse:
        genres = self.genre_repository.list()

        sorted_data = sorted([
            GenreOutput(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories=genre.categories
            )
            for genre in genres
        ], key=lambda genre: getattr(genre, request.order_by))

        page_offset = (request.current_page -1) * request.per_page
        genres_page = sorted_data[page_offset:page_offset + request.per_page]

        return ListGenreResponse(
            data=genres_page,
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=request.per_page,
                total=len(sorted_data)
            )
        )