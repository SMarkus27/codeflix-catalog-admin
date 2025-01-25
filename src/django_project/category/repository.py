from uuid import UUID

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.django_project.category.models import Category as CategoryModel


class DjangoORMCategoryRepository(CategoryRepository):

    def __init__(self, model: CategoryModel | None = None):
        self.model = model or CategoryModel

    def save(self, category: Category) -> None:
        self.model.objects.create(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category = self.model.objects.get(id=id)
            return Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active
            )

        except self.model.DoesNotExist:
            return None

    def list(self) -> list[Category]:
        return [
            Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active
            )
            for category in self.model.objects.all()
        ]

    def delete(self, id: UUID) -> None:
        self.model.objects.filter(id=id).delete()

    def update(self, category: Category) -> None:
        self.model.objects.filter(pk=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )