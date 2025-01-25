from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, \
    HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet

from src.core.genre.application.exceptions import InvalidGenre, RelatedCategoriesNotFound, GenreNotFound
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.django_project.category.repository import DjangoORMCategoryRepository
from src.django_project.genre.repository import DjangoORMGenreRepository
from src.django_project.genre.serializers import ListGenreResponseSerializer, CreateGenreInputSerializer, \
    CreateGenreResponseSerializer, DeleteGenreInputSerializer


class GenreViewSet(ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListGenre(DjangoORMGenreRepository())
        output = use_case.execute(input=ListGenre.Input())
        response = ListGenreResponseSerializer(output)

        return Response(
            status=HTTP_200_OK,
            data=response.data
        )

    def create(self, request: Request) -> Response:
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateGenre(category_repository=DjangoORMCategoryRepository(),
                               genre_repository=DjangoORMGenreRepository())

        try:
            output = use_case.execute(CreateGenre.Input(**serializer.validated_data))

        except (InvalidGenre, RelatedCategoriesNotFound) as err:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(err)}
            )

        return Response(
            status=HTTP_201_CREATED,
            data=CreateGenreResponseSerializer(output).data
        )


    def destroy(self, request: Request, pk=None) -> Response:
        request_data = DeleteGenreInputSerializer(data={"id": pk})
        request_data.is_valid(raise_exception=True)

        input = DeleteGenre.Input(**request_data.validated_data)
        use_case = DeleteGenre(DjangoORMGenreRepository())
        try:
            use_case.execute(input)
        except GenreNotFound as err:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)