from dataclasses import dataclass, field
from uuid import UUID

from src.config import DEFAULT_PER_PAGE_SIZE
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository

@dataclass
class ListCastMemberRequest:
    order_by: str = "name"
    current_page: int = 1
    per_page: int = DEFAULT_PER_PAGE_SIZE

@dataclass
class ListOutputMeta:
    current_page: int
    per_page: int
    total: int

@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType

@dataclass
class ListCastMemberResponse:
    data: list[CastMemberOutput]
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)


class ListCastMember:
    def __init__(self, cast_member_repository: CastMemberRepository):
        self.cast_member_repository = cast_member_repository

    def execute(self, request: ListCastMemberRequest) -> ListCastMemberResponse:
        cast_members = self.cast_member_repository.list()
        sorted_data = sorted([
            CastMemberOutput(
                id=cast_member.id,
                    name=cast_member.name,
                    type=cast_member.type
                ) for cast_member in cast_members
        ], key=lambda category: getattr(category, request.order_by)
        )

        page_offset = (request.current_page -1) * request.per_page
        categories_page = sorted_data[page_offset:page_offset + request.per_page]


        return ListCastMemberResponse(
            data=categories_page,
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=request.per_page,
                total=len(sorted_data)
            )
        )
