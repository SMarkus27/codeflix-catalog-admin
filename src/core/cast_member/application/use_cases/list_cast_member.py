from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository

@dataclass
class ListCastMemberRequest:
    ...

@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType

@dataclass
class ListCastMemberResponse:
    data: list[CastMemberOutput]



class ListCastMember:
    def __init__(self, cast_member_repository: CastMemberRepository):
        self.cast_member_repository = cast_member_repository

    def execute(self, request: ListCastMemberRequest) -> ListCastMemberResponse:
        cast_members = self.cast_member_repository.list()

        return ListCastMemberResponse(
            data = [
                CastMemberOutput(
                    id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type
                ) for cast_member in cast_members
        ])
