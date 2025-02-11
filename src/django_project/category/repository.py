from uuid import UUID

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.django_project.category.models import Category as CategoryModel


class DjangoORMCategoryRepository(CategoryRepository):

    def __init__(self, model: CategoryModel | None = None):
        self.model = model or CategoryModel

    def save(self, category: Category) -> None:
        category_model = CategoryModelMapper.to_model(category)
        category_model.save()

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category_model = self.model.objects.get(id=id)
            return CategoryModelMapper.to_entity(category_model)

        except self.model.DoesNotExist:
            return None

    def list(self) -> list[Category]:
        return [
            CategoryModelMapper.to_entity(category_model)
            for category_model in self.model.objects.all()
        ]

    def delete(self, id: UUID) -> None:
        self.model.objects.filter(id=id).delete()

    def update(self, category: Category) -> None:
        self.model.objects.filter(pk=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

class CategoryModelMapper:

    @staticmethod
    def to_model(category: Category) -> CategoryModel:
        return CategoryModel(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )

    @staticmethod
    def to_entity(category_model: CategoryModel) -> Category:
        return Category(
            id=category_model.id,
            name=category_model.name,
            description=category_model.description,
            is_active=category_model.is_active
        )