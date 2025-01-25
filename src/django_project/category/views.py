from uuid import UUID

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
    HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet

from src.core.category.application.use_cases.create_category import CreateCategoryRequest, CreateCategory
from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from src.core.category.application.use_cases.list_category import ListCategoryRequest, ListCategory
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.django_project.category.repository import DjangoORMCategoryRepository
from src.django_project.category.serializers import ListCategoryResponseSerializer, RetrieveCategoryRequestSerializer, \
    RetrieveCategoryResponseSerializer, CreateCategoryRequestSerializer, \
    CreateCategoryResponseSerializer, UpdateCategoryRequestSerializer, DeleteCategoryRequestSerializer, \
    UpdatePartialCategoryRequestSerializer


class CategoryViewSet(ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCategoryRequest()
        use_case = ListCategory(DjangoORMCategoryRepository())
        response = use_case.execute(input)

        serializer = ListCategoryResponseSerializer(instance=response)

        return Response(
            status=HTTP_200_OK,
            data=serializer.data
        )

    def retrieve(self, request: Request, pk=None) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = GetCategory(DjangoORMCategoryRepository())

        try:
            result = use_case.execute(GetCategoryRequest(serializer.validated_data["id"]))

        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category = RetrieveCategoryResponseSerializer(instance=result)

        return Response(
            status=HTTP_200_OK,
            data=category.data
        )

    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCategoryRequest(**serializer.validated_data)
        use_case = CreateCategory(DjangoORMCategoryRepository())
        output = use_case.execute(input)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateCategoryResponseSerializer(instance=output).data
        )

    def update(self, request: Request, pk=None) -> Response:
        serializer = UpdateCategoryRequestSerializer(
            data={**request.data,
                  "id": pk}
        )

        serializer.is_valid(raise_exception=True)
        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(DjangoORMCategoryRepository())
        use_case.execute(input)

        return Response(status=HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk=None) -> Response:
        serializer = DeleteCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = DeleteCategory(DjangoORMCategoryRepository())
        try:
            use_case.execute(DeleteCategoryRequest(**serializer.validated_data))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk: UUID = None) -> Response:
        serializer = UpdatePartialCategoryRequestSerializer(
            data={**request.data,
                  "id": pk}
        )

        serializer.is_valid(raise_exception=True)
        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(DjangoORMCategoryRepository())
        use_case.execute(input)

        return Response(status=HTTP_204_NO_CONTENT)