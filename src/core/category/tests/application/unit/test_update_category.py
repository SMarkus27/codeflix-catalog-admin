from unittest.mock import create_autospec

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.domain.category import Category


class TestUpdateCategory:

    def test_update_category_name(self):
        category = Category("filme", "Categoria para filmes")
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(category.id, name="Serie")

        use_case.execute(request)

        assert category.name == "Serie"
        assert category.description == "Categoria para filmes"

        mock_repository.update.assert_called_once_with(category)

    def test_update_category_description(self):
        category = Category("filme", "Categoria para filmes")
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(category.id, description="Serie em geral")

        use_case.execute(request)

        assert category.name == "filme"
        assert category.description == "Serie em geral"

        mock_repository.update.assert_called_once_with(category)

    def test_can_deactivate_category(self):
        category = Category("filme", "Categoria para filmes")
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(category.id, is_active=False)

        use_case.execute(request)

        assert category.is_active is False
        mock_repository.update.assert_called_once_with(category)

    def test_cam_activate_category(self):
        category = Category("filme", "Categoria para filmes", False)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(category.id, is_active=True)

        use_case.execute(request)

        assert category.is_active is True
        mock_repository.update.assert_called_once_with(category)
