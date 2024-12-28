from uuid import uuid4

import pytest

from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestGetCategory:
    def test_get_category(self):
        category = Category("filme", "categoria para filme")
        repository = InMemoryCategoryRepository([category])

        use_case = GetCategory(repository)
        request = GetCategoryRequest(category.id)

        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            category.id, "filme", "categoria para filme", True
        )

    def test_when_category_does_exist_then_raise_exception(self):
        category = Category("filme", "categoria para filme")
        repository = InMemoryCategoryRepository([category])

        use_case = GetCategory(repository)
        request = GetCategoryRequest(uuid4())

        with pytest.raises(CategoryNotFound) as err:
            use_case.execute(request)
