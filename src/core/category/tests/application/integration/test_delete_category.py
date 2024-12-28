from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestDeleteCategory:
    def test_delete_category(self):
        category = Category("filme", "categoria para filme")
        repository = InMemoryCategoryRepository([category])

        use_case = DeleteCategory(repository)
        request = DeleteCategoryRequest(category.id)

        assert repository.get_by_id(category.id) is not None

        response = use_case.execute(request)

        assert repository.get_by_id(category.id) is None
        assert response is None
