from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.cast_member.application.exceptions import CastMemberNotFound, InvalidCastMember
from src.core.cast_member.application.use_cases.update_cast_member import UpdateCastMember, UpdateCastMemberRequest
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


@pytest.fixture
def actor():
    return CastMember(
        name="Bruce Willis",
        type=CastMemberType.ACTOR
    )


class TestUpdateCastMember:

    def test_update_cast_member(self, actor):
        cast_member_repository = InMemoryCastMemberRepository()
        cast_member_repository.save(actor)

        use_case = UpdateCastMember(cast_member_repository)

        request = UpdateCastMemberRequest(
            id=actor.id,
            name="John Smith",
            type=CastMemberType.ACTOR
        )

        use_case.execute(request)

        cast_member_updated = cast_member_repository.get_by_id(actor.id)

        assert cast_member_updated.name == "John Smith"
        assert cast_member_updated.type == "ACTOR"


    def test_update_cast_member_when_cast_not_exist_raise_exception(self, actor):
        cast_member_repository = InMemoryCastMemberRepository()

        cast_member_repository.save(actor)

        use_case = UpdateCastMember(cast_member_repository)

        request = UpdateCastMemberRequest(
            id=uuid4(),
            name="John Smith",
            type=CastMemberType.ACTOR
        )
        with pytest.raises(CastMemberNotFound):
            use_case.execute(request)


    def test_update_cast_member_with_invalid_name_then_raise_exception(self, actor):
        cast_member_repository = InMemoryCastMemberRepository()

        cast_member_repository.save(actor)

        use_case = UpdateCastMember(cast_member_repository)


        with pytest.raises(InvalidCastMember):
            request = UpdateCastMemberRequest(
                id=actor.id,
                name="",
                type=CastMemberType.ACTOR
            )

            use_case.execute(request)




    def test_update_cast_member_with_invalid_type_then_raise_exception(self, actor):
        cast_member_repository = InMemoryCastMemberRepository()

        cast_member_repository.save(actor)

        use_case = UpdateCastMember(cast_member_repository)

        with pytest.raises(InvalidCastMember):
            request = UpdateCastMemberRequest(
                id=actor.id,
                name="John Smith",
                type=""
            )

            use_case.execute(request)
