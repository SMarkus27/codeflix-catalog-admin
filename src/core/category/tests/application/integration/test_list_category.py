from src.core._shared.list import ListRequest
from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryResponse,
    CategoryOutput, ListOutputMeta,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestListCategory:
    def test_empty_list(self):

        mock_repository = InMemoryCategoryRepository([])

        use_case = ListCategory(mock_repository)
        request = ListRequest()

        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=0
            )
        )

    def test_list_category(self):
        category1 = Category(name="filme", description="Categoria para filmes")

        category2 = Category(name="Serie", description="Categoria para Series")
        repository = InMemoryCategoryRepository()
        repository.save(category1)
        repository.save(category2)

        use_case = ListCategory(repository)
        request = ListRequest()

        response = use_case.execute(request)
        print(response)
        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    category2.id,
                    category2.name,
                    category2.description,
                    category2.is_active,
                ),
                CategoryOutput(
                    category1.id,
                    category1.name,
                    category1.description,
                    category1.is_active,
                ),

            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=2
            )
        )
