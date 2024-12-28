from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest,
    ListCategoryResponse,
    CategoryOutput,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestListCategory:
    def test_empty_list(self):

        mock_repository = InMemoryCategoryRepository([])

        use_case = ListCategory(mock_repository)
        request = ListCategoryRequest()

        response = use_case.execute(request)

        assert response == ListCategoryResponse(data=[])

    def test_list_category(self):
        category1 = Category("filme", "Categoria para filmes")

        category2 = Category("Serie", "Categoria para Series")
        repository = InMemoryCategoryRepository()
        repository.save(category1)
        repository.save(category2)

        use_case = ListCategory(repository)
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
