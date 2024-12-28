from uuid import UUID

from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
)
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository)
        request = CreateCategoryRequest("filme", "Categoria para filme", True)

        response = use_case.execute(request)

        assert response.id is not None
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1

        assert repository.categories[0].id == response.id
        assert repository.categories[0].name == "filme"
        assert repository.categories[0].description == "Categoria para filme"
        assert repository.categories[0].is_active is True
