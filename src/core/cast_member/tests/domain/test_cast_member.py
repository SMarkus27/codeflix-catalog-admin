from uuid import UUID

import pytest

from src.core.cast_member.domain.cast_member import CastMember


class TestCastMember:

    def test_create_cast_member(self):
        cast_member = CastMember(name="Bruce Willis", type="ACTOR")

        assert cast_member.name == "Bruce Willis"
        assert cast_member.type == "ACTOR"
        assert isinstance(cast_member.id, UUID)

    def test_cannot_create_cast_member_with_empty_name(self):
        with pytest.raises(ValueError, match="Name cannot be empty"):
            CastMember(name="", type="ACTOR")

    def test_cannot_create_cast_member_with_invalid_type(self):
        with pytest.raises(ValueError, match="Cast member type must be DIRECTOR or ACTOR"):
            CastMember(name="Bruce Willis", type="WRITER")
