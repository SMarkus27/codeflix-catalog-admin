import pytest

from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_edit_category(self):
        api_client = APIClient()

        list_response = api_client.get("/api/categories/")
        assert list_response.data == {"data": []}

        create_response = api_client.post(
            "/api/categories/",
            data={
                "name": "Movie",
                "description": "Movie description"
            })

        assert create_response.status_code == 201
        create_category_id = create_response.data["id"]

        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {
                    "id": create_category_id,
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True
                }

        ]}

        update_response = api_client.put(
            f"/api/categories/{create_category_id}/",
            data={
                "name": "Serie",
                "description": "Serie description",
                "is_active": False
            })

        assert update_response.status_code == 204

        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {
                    "id": create_category_id,
                    "name": "Serie",
                    "description": "Serie description",
                    "is_active": False
                }

            ]}


