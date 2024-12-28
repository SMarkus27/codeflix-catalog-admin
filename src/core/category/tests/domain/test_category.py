from uuid import UUID, uuid4

import pytest

from src.core.category.domain.category import Category


class TestCategory:

    def test_name_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'name'"
        ):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            Category(name="a" * 256)

    def test_category_must_be_created_with_id_as_uuid_by_default(self):
        category = Category(name="Filme")
        assert isinstance(category.id, UUID)

    def test_create_category_with_default_values(self):
        category = Category(name="Filme")

        assert category.name == "Filme"
        assert category.description == ""

    def test_create_category_as_active_by_default(self):
        category = Category(name="Filme")
        assert category.is_active is True

    def test_create_category_with_providers_values(self):
        cat_id = uuid4()
        category = Category(
            id=cat_id, name="Filme", description="Filmes em geral", is_active=False
        )

        assert category.id == cat_id
        assert category.name == "Filme"
        assert category.description == "Filmes em geral"
        assert category.is_active is False

    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")


class TesUpdateCategory:

    def test_update_category_with_name_and_description(self):
        category = Category(name="Filme", description="Filmes em geral")
        category.update_category(name="Serie", description="Series em geral")

        assert category.name == "Serie"
        assert category.description == "Series em geral"

    def test_update_category_with_invalid_name(self):
        category = Category(name="Filme", description="Filmes em geral")
        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            category.update_category(name="a" * 256, description="Series em geral")

    def test_cannot_update_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")


class TestActivate:
    def test_activate_category(self):
        category = Category(
            name="Filme", description="Filmes em geral", is_active=False
        )

        category.activate()

        assert category.is_active is True
