
import pytest

from src.core.cast_member.application.use_cases.list_cast_member import ListCastMember, ListCastMemberRequest
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository

@pytest.fixture
def actor():
    return CastMember(
        name="Bruce Willis",
        type=CastMemberType.ACTOR
    )

@pytest.fixture
def director():
    return CastMember(
        name="Ron Russo",
        type=CastMemberType.DIRECTOR
    )


class TestListCastMember:

    def test_list_cast_member(self, actor, director):
        cast_member_reṕository = InMemoryCastMemberRepository()
        cast_member_reṕository.save(actor)
        cast_member_reṕository.save(director)

        use_case = ListCastMember(cast_member_reṕository)

        response = use_case.execute(ListCastMemberRequest())

        assert len(response.data) == 2
        assert response.data[0].name == "Bruce Willis"
        assert response.data[0].type == "ACTOR"

        assert response.data[1].name == "Ron Russo"
        assert response.data[1].type == "DIRECTOR"


    def test_list_no_cast_member_return_empty_list(self):
        cast_member_reṕository = InMemoryCastMemberRepository()
        use_case = ListCastMember(cast_member_reṕository)
        response = use_case.execute(ListCastMemberRequest())

        assert response.data == []
