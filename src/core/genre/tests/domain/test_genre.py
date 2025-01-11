from uuid import UUID, uuid4

import pytest

from src.core.genre.domain.genre import Genre


class TestGenre:

    def test_name_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'name'"
        ):
            Genre()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            Genre(name="a" * 256)


    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Genre(name="")


    def test_create_genre_with_default_values(self):
        genre = Genre(name="Action")

        assert isinstance(genre.id, UUID)
        assert genre.name == "Action"
        assert genre.is_active is True
        assert genre.categories == set()


    def test_create_category_with_providers_values(self):
        genre_id = uuid4()
        categories = {uuid4(), uuid4()}

        genre = Genre(
            id=genre_id,
            name="Action",
            is_active=False,
            categories=categories
        )

        assert genre.id == genre_id
        assert genre.name == "Action"
        assert genre.is_active is False
        assert genre.categories == categories



class TestActivate:
    def test_activate_genre(self):
        genre = Genre(
            name="Action",
            is_active=False
        )

        genre.activate()

        assert genre.is_active is True


class TestDeactivate:
    def test_deactivate_genre(self):
        genre = Genre(
            name="Action",
            is_active=True
        )

        genre.deactivate()

        assert genre.is_active is False


class TestChangeName:
    def test_change_name(self):
        genre = Genre(name="Action")

        genre.change_name("Adventure")

        assert genre.name == "Adventure"

    def test_change_name_with_invalid_name(self):
        genre = Genre(name="Action")

        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            genre.change_name("a" * 256)

    def test_cannot_change_name_with_empty_name(self):
        genre = Genre(name="Action")

        with pytest.raises(ValueError, match="name cannot be empty"):
            genre.change_name("")

class TestAddCategory:
    def test_add_category_to_genre(self):
        genre = Genre(name="Action")
        category_id = uuid4()

        assert category_id not in genre.categories
        genre.add_category(uuid4())

        assert category_id in genre.categories


class TestRemoveCategory:
    def test_remove_category_to_genre(self):
        genre = Genre(name="Action")
        category_id = uuid4()

        genre.add_category(category_id)
        assert category_id in genre.categories

        genre.remove_category(category_id)
        assert category_id not in genre.categories