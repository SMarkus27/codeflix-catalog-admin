from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class InMemoryCastMemberRepository(CastMemberRepository):

    def __init__(self, cast_member=None):
        self.cast_member = cast_member or []

    def save(self, cast_member: CastMember) -> None:
        self.cast_member.append(cast_member)

    def get_by_id(self, id: UUID) -> CastMember:
        for cast_member in self.cast_member:
            if cast_member.id == id:
                return cast_member

        return None

    def list(self) -> list[CastMember]:
        return [cast_member for cast_member in self.cast_member]

    def delete(self, id: UUID) -> None:
        cast_member = self.get_by_id(id)
        self.cast_member.remove(cast_member)

    def update(self, cast_member: CastMember) -> None:
        old_cast_member = self.get_by_id(cast_member.id)
        if old_cast_member:
            self.cast_member.remove(old_cast_member)
            self.cast_member.append(cast_member)
