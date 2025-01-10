from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestUpdateCategory:

    def test_can_update_category_name_and_description(self):
        category = Category("filme", "Categoria para filmes")
        repository = InMemoryCategoryRepository([category])
        repository.save(category)

        use_case = UpdateCategory(repository)
        request = UpdateCategoryRequest(
            category.id, name="Serie", description="Serie em geral"
        )

        use_case.execute(request)

        updated_category = repository.get_by_id(category.id)

        assert updated_category.name == "Serie"
        assert updated_category.description == "Serie em geral"
