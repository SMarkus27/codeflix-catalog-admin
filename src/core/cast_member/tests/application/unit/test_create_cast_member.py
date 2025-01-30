from unittest.mock import create_autospec
from uuid import UUID

import pytest

from src.core.cast_member.application.exceptions import InvalidCastMember
from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember, CreateCastMemberRequest
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestCreateCastMember:

    def test_create_cast_member(self):
        cast_member_repository = create_autospec(CastMemberRepository)

        use_case = CreateCastMember(cast_member_repository)

        request = CreateCastMemberRequest(
            name="Bruce Willis",
            type=CastMemberType.ACTOR
        )

        response = use_case.execute(request)

        assert isinstance(response.id, UUID)


    def test_create_cast_member_with_invalid_name(self):
        cast_member_repository = create_autospec(CastMemberRepository)

        use_case = CreateCastMember(cast_member_repository)

        with pytest.raises(InvalidCastMember, match="Name cannot be empty"):
            request = CreateCastMemberRequest(
                name="",
                type=CastMemberType.ACTOR
            )
            use_case.execute(request)


    def test_create_cast_member_with_invalid_cast_member_type(self):
        cast_member_repository = create_autospec(CastMemberRepository)

        use_case = CreateCastMember(cast_member_repository)

        with pytest.raises(InvalidCastMember, match="Cast member type must be DIRECTOR or ACTOR"):
            request = CreateCastMemberRequest(
                name="Bruce Willis",
                type=""
            )
            use_case.execute(request)
