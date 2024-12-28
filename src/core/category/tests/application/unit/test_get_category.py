from unittest.mock import MagicMock

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)
from src.core.category.domain.category import Category


class TestGetCategory:
    def test_get_category(self):
        category = Category("filme", "Categoria para filmes")
        mock_repository = MagicMock(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = GetCategory(mock_repository)
        request = GetCategoryRequest(category.id)

        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            category.id, "filme", "Categoria para filmes", True
        )
