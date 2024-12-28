from unittest.mock import create_autospec

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest,
    ListCategoryResponse,
    CategoryOutput,
)
from src.core.category.domain.category import Category


class TestListCategory:
    def test_empty_list(self):

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = []

        use_case = ListCategory(mock_repository)
        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[],
        )

    def test_list_category(self):
        category1 = Category("filme", "Categoria para filmes")

        category2 = Category("Serie", "Categoria para Series")
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = [category1, category2]

        use_case = ListCategory(mock_repository)
        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    category1.id,
                    category1.name,
                    category1.description,
                    category1.is_active,
                ),
                CategoryOutput(
                    category2.id,
                    category2.name,
                    category2.description,
                    category2.is_active,
                ),
            ]
        )
