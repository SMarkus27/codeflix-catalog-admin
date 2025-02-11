from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class ListCategoryRequest:
    order_by: str = "name"
    current_page: int = 1


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


@dataclass
class ListOutputMeta:
    current_page: int
    per_page: int
    total: int

@dataclass
class ListCategoryResponse:
    data: list[CategoryOutput]
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)


class ListCategory:

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: ListCategoryRequest) -> ListCategoryResponse:
        categories = self.repository.list()
        sorted_data = sorted([
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active
                )
                for category in categories
            ], key=lambda category: getattr(category, request.order_by))

        page_offset = (request.current_page -1) * 2
        categories_page = sorted_data[page_offset:page_offset + 2]


        return ListCategoryResponse(
            data=categories_page,
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=2,
                total=len(sorted_data)
            )
        )
