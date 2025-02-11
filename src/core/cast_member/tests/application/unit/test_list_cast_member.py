from unittest.mock import create_autospec

import pytest

from src.core.cast_member.application.use_cases.list_cast_member import ListCastMember, ListCastMemberRequest
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@pytest.fixture
def mock_cast_member_repository() -> CastMemberRepository:
    actor = CastMember(
        name="Bruce Willis",
        type=CastMemberType.ACTOR
    )

    director = CastMember(
        name="Ron Russo",
        type=CastMemberType.DIRECTOR
    )

    cast_member_repository = create_autospec(CastMemberRepository)
    cast_member_repository.list.return_value = [actor, director]
    return cast_member_repository

@pytest.fixture
def mock_empty_repository() -> CastMemberRepository:
    cast_member_repository = create_autospec(CastMemberRepository)
    cast_member_repository.list.return_value = []
    return cast_member_repository

class TestListCastMember:

    def test_list_cast_member(self, mock_cast_member_repository: CastMemberRepository):
        use_case = ListCastMember(mock_cast_member_repository)

        response = use_case.execute(ListCastMemberRequest())

        assert len(response.data) == 2
        assert response.data[0].name == "Bruce Willis"
        assert response.data[0].type == "ACTOR"

        assert response.data[1].name == "Ron Russo"
        assert response.data[1].type == "DIRECTOR"


    def test_list_no_cast_member_return_empty_list(self, mock_empty_repository: CastMemberRepository):
        use_case = ListCastMember(mock_empty_repository)
        response = use_case.execute(ListCastMemberRequest())

        assert response.data == []
