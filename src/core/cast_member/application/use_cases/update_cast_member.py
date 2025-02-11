from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.exceptions import CastMemberNotFound, InvalidCastMember
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class UpdateCastMemberRequest:
    id: UUID
    name: str
    type: CastMemberType


class UpdateCastMember:
    def __init__(self, cast_member: CastMemberRepository):
        self.cast_member = cast_member

    def execute(self, request: UpdateCastMemberRequest) -> None:
        cast_member = self.cast_member.get_by_id(request.id)
        if cast_member is None:
            raise CastMemberNotFound(f"Cast member with {request.id} not found")

        try:
            cast_member.update_cast_member(request.name, request.type)
        except ValueError as err:
            raise InvalidCastMember(err)

        self.cast_member.update(cast_member)
