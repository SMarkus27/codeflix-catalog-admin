from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class DeleteCastMemberRequest:
    id: UUID


class DeleteCastMember:

    def __init__(self, cast_member: CastMemberRepository):
        self.cast_member = cast_member

    def execute(self, request: DeleteCastMemberRequest) -> None:
        cast_member = self.cast_member.get_by_id(request.id)
        if cast_member is None:
            raise CastMemberNotFound(f"Cast member with {request.id} not found")

        self.cast_member.delete(cast_member.id)
