from uuid import uuid4

import pytest

from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember, DeleteCastMemberRequest
from src.core.cast_member.domain.cast_member import CastMemberType, CastMember
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestDeleteCastMember:

    def test_delete_cast_member_when_cast_not_exist(self):
        cast_member_repository = InMemoryCastMemberRepository()

        use_case = DeleteCastMember(cast_member_repository)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(DeleteCastMemberRequest(uuid4()))


    def test_delete_cast_member(self):
        cast_member_repository = InMemoryCastMemberRepository()

        cast_member = CastMember(
            name="Bruce Willis",
            type=CastMemberType.ACTOR
        )

        cast_member_repository.save(cast_member)

        use_case = DeleteCastMember(cast_member_repository)

        assert cast_member_repository.get_by_id(cast_member.id) is not None

        use_case.execute(DeleteCastMemberRequest(cast_member.id))

        assert cast_member_repository.get_by_id(cast_member.id) is None
