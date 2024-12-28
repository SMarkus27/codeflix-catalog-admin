import uuid
from uuid import uuid4

import pytest
from rest_framework.test import APITestCase, APIClient

from core.category.domain.category import Category
from src.django_project.category.repository import DjangoORMCategoryRepository


@pytest.fixture
def category_movie():
    return Category("movie", "movie description")


@pytest.fixture
def category_serie():
    return Category("serie", "serie description")


@pytest.fixture
def category_repository():
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestCategoryAPI:
    def test_list_categories(self, category_movie: Category, category_serie: Category, category_repository: DjangoORMCategoryRepository):
        repository = category_repository
        repository.save(category_movie)
        repository.save(category_serie)

        url = "/api/categories/"
        response = APIClient().get(url)

        expected_data = {
            "data": [
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active
                },
                {
                    "id": str(category_serie.id),
                    "name": category_serie.name,
                    "description": category_serie.description,
                    "is_active": category_serie.is_active
                }
            ]
        }

        assert response.status_code == 200
        assert response.data == expected_data


@pytest.mark.django_db
class TestRetrieveAPI:

    def test_when_id_is_invalid(self):
        url = "/api/categories/1234/"
        response = APIClient().get(url)

        assert response.status_code == 400

    def test_return_category_when_exist(self, category_movie: Category, category_serie: Category, category_repository: DjangoORMCategoryRepository):
        repository = category_repository
        repository.save(category_movie)
        repository.save(category_serie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().get(url)

        expected_data = {
            "data": {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active
            }
        }

        assert response.status_code == 200
        assert response.data == expected_data

    def test_return_404_when_not_exist(self):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().get(url)

        assert response.status_code == 404


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        url = f"/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "",
                "description": "Movie description"
            }
        )

        assert response.status_code == 400
        assert response.data == {
            "name": ["This field may not be blank."]
        }

    def test_when_payload_is_valid_then_create_category(self, category_repository: DjangoORMCategoryRepository):
        url = f"/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "Movie",
                "description": "Movie description"
            }
        )

        assert response.status_code == 201
        assert category_repository.list() == [
            Category(
                id=uuid.UUID(response.data["id"]),
                name="Movie",
                description="Movie description",

            )
        ]


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        url = f"/api/categories/1212212/"
        response = APIClient().put(
            url,
            data={
                "name": "",
                "description": "Movie description"
            }
        )

        assert response.status_code == 400
        assert response.data == {
            "name": ["This field may not be blank."],
            "id": ["Must be a valid UUID."],
            "is_active": ["This field is required."]
        }

    def test_when_payload_is_valid_then_update_category_and_return_204(self, category_movie: Category, category_repository: DjangoORMCategoryRepository):
        category_repository.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"

        response = APIClient().put(
            url,
            data={
                "name": "Serie",
                "description": "Serie description",
                "is_active": True

            }
        )

        assert response.status_code == 204

        expected_category = Category(
            id=category_movie.id,
            name=category_movie.name,
            description=category_movie.description,
            is_active=True
        )

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.name == "Serie"
        assert updated_category.description == "Serie description"
        assert updated_category.is_active is True


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_id_is_invalid(self):
        url = "/api/categories/1234223/"
        response = APIClient().delete(url)

        assert response.status_code == 400

    def test_when_category_does_not_exist_then_return_404(self):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == 404

    def test_when_category_does_exist_then_delete_and_return_204(self, category_movie: Category,
                                                                 category_repository: DjangoORMCategoryRepository):
        category_repository.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"

        response = APIClient().delete(url)

        assert response.status_code == 204
        assert category_repository.list() == []


@pytest.mark.django_db
class TestUpdatePartialAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        url = f"/api/categories/1212212/"
        response = APIClient().patch(
            url,
            data={
                "name": "",
                "description": "Movie description"
            }
        )

        assert response.status_code == 400
        assert response.data == {
            "name": ["This field may not be blank."],
            "id": ["Must be a valid UUID."]
        }

    def test_when_payload_has_only_name_then_update_category_and_return_204(self, category_movie: Category, category_repository: DjangoORMCategoryRepository):
        category_repository.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"

        response = APIClient().patch(
            url,
            data={
                "name": "Serie",
            }
        )

        assert response.status_code == 204

        expected_category = Category(
            id=category_movie.id,
            name=category_movie.name,
            description=category_movie.description,
            is_active=True
        )

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.name == "Serie"
        assert updated_category.description == "movie description"
        assert updated_category.is_active is True

    def test_when_payload_has_only_description_then_update_category_and_return_204(self, category_movie: Category, category_repository: DjangoORMCategoryRepository):
        category_repository.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"

        response = APIClient().patch(
            url,
            data={
                "description": "Serie description",
            }
        )

        assert response.status_code == 204

        expected_category = Category(
            id=category_movie.id,
            name=category_movie.name,
            description=category_movie.description,
            is_active=True
        )

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.name == "movie"
        assert updated_category.description == "Serie description"
        assert updated_category.is_active is True

    def test_when_payload_has_only_is_active_then_update_category_and_return_204(self, category_movie: Category, category_repository: DjangoORMCategoryRepository):
        category_repository.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"

        response = APIClient().patch(
            url,
            data={
                "is_active": False,
            }
        )

        assert response.status_code == 204

        expected_category = Category(
            id=category_movie.id,
            name=category_movie.name,
            description=category_movie.description,
            is_active=True
        )

        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.name == "movie"
        assert updated_category.description == "movie description"
        assert updated_category.is_active is False