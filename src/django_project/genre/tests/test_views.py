from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category.repository import DjangoORMCategoryRepository
from src.django_project.genre.repository import DjangoORMGenreRepository


@pytest.fixture
def category_movie():
    return Category(name="Movie", description="Movie description")

@pytest.fixture
def category_serie():
    return Category(name="Serie", description="Serie description")

@pytest.fixture
def category_repository(category_movie, category_serie) -> DjangoORMCategoryRepository:
    repository = DjangoORMCategoryRepository()
    repository.save(category_movie)
    repository.save(category_serie)
    return repository

@pytest.fixture
def genre_action(category_movie, category_serie) -> Genre:
    return Genre(name="Action", categories={category_movie.id, category_serie.id})

@pytest.fixture
def genre_terror() -> Genre:
    return Genre(name="Terror", categories=set())

@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()

@pytest.mark.django_db
class TestListAPI:
    def test_list_genres_and_categories(self,
                                        genre_action,
                                        genre_terror,
                                        genre_repository,
                                        category_repository,
                                        category_movie,
                                        category_serie):

        genre_repository.save(genre_action)
        genre_repository.save(genre_terror)

        url = "/api/genres/"
        response = APIClient().get(url)

        # expected_response = {
        #     "data": [
        #         {
        #             "id": str(genre_action.id),
        #             "name": "Action",
        #             "is_active": True,
        #             "categories": [str(category_movie.id), str(category_serie.id)]
        #         },
        #         {
        #             "id": str(genre_terror.id),
        #             "name": "Terror",
        #             "is_active": True,
        #             "categories": []
        #         }
        #     ]
        # }
        #
        #
        # assert response.status_code == 200
        # assert response == expected_response

        assert response.status_code == 200
        data = response.data["data"]

        assert data[0]["id"] == str(genre_action.id)
        assert data[0]["name"] == "Action"
        assert data[0]["is_active"] is True
        assert set(data[0]["categories"]) == {str(category_movie.id), str(category_serie.id)}

        assert data[1]["id"] == str(genre_terror.id)
        assert data[1]["name"] == "Terror"
        assert data[1]["is_active"] is True
        assert data[1]["categories"] == []


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_genre_with_associated_categories(
            self,
            category_movie,
            category_serie,
            category_repository,
            genre_repository
    ):

        url = "/api/genres/"
        data = {
            "name": "Adventure",
            "categories": [str(category_movie.id), str(category_serie.id)]
        }

        response = APIClient().post(url, data=data)

        assert response.status_code == 201

        genre_id = response.data["id"]

        genre = genre_repository.get_by_id(genre_id)

        assert genre.name == "Adventure"
        assert genre.categories == {category_movie.id, category_serie.id}

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = "/api/genres/"
        data = {
            "name": "",
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == 400
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
    ) -> None:
        url = "/api/genres/"
        data = {
            "name": "Romance",
            "categories": [uuid4()],
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == 400
        assert "Categories with provided IDs not found" in response.data["error"]

@pytest.mark.django_db
class TestDeleteAPI:

    def test_when_genre_does_not_exist_then_return_404(self):
        url = f"/api/genres/{uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == 404

    def test_when_pk_is_invalid_uuid_then_return_400(self):
        url = f"/api/genres/1/"
        response = APIClient().delete(url)

        assert response.status_code == 400

    def test_when_genre_found_then_delete_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_serie: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_terror: Genre,
    ) -> None:
        genre_repository.save(genre_terror)

        url = f"/api/genres/{str(genre_terror.id)}/"
        response = APIClient().delete(url)

        assert response.status_code == 204
        assert genre_repository.get_by_id(genre_terror.id) is None


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_serie: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_terror: Genre,
    ) -> None:
        genre_repository.save(genre_terror)

        url = f"/api/genres/{str(genre_terror.id)}/"
        data = {
            "name": "Drama",
            "is_active": True,
            "categories": [category_serie.id],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == 204
        updated_genre = genre_repository.get_by_id(genre_terror.id)
        assert updated_genre.name == "Drama"
        assert updated_genre.is_active is True
        assert updated_genre.categories == {category_serie.id}

    def test_when_request_data_is_invalid_then_return_400(
        self,
        genre_action: Genre,
    ) -> None:
        url = f"/api/genres/{str(genre_action.id)}/"
        data = {
            "name": "",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == 400
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_serie: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_terror: Genre,
    ) -> None:
        genre_repository.save(genre_terror)

        url = f"/api/genres/{str(genre_terror.id)}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [uuid4()],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == 400
        assert "Categories with provided IDs not found" in response.data["error"]

    def test_when_genre_does_not_exist_then_return_404(self) -> None:
        url = f"/api/genres/{str(uuid4())}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == 404