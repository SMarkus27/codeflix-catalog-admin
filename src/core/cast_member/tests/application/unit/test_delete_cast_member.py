from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember, DeleteCastMemberRequest
from src.core.cast_member.domain.cast_member import CastMemberType, CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository



class TestDeleteCastMember:

    def test_delete_cast_member_when_cast_not_exist(self):
        mock_cast_member_repository = create_autospec(CastMemberRepository)
        mock_cast_member_repository.get_by_id.return_value = None

        use_case = DeleteCastMember(mock_cast_member_repository)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(DeleteCastMemberRequest(uuid4()))


    def test_delete_cast_member(self):
        cast_member = CastMember(
            name="Bruce Willis",
            type=CastMemberType.ACTOR
        )

        mock_cast_member_repository = create_autospec(CastMemberRepository)
        mock_cast_member_repository.get_by_id.return_value = cast_member

        use_case = DeleteCastMember(mock_cast_member_repository)

        use_case.execute(DeleteCastMemberRequest(cast_member.id))
        mock_cast_member_repository.delete.assert_called_once_with(cast_member.id)