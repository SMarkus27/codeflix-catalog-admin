from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID, uuid4


class CastMemberType(StrEnum):
    DIRECTOR = "DIRECTOR"
    ACTOR = "ACTOR"

@dataclass
class CastMember:
    name: str
    type: CastMemberType
    id: UUID = field(default_factory=uuid4)



    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) == 0:
            raise ValueError("Name cannot be empty")

        if len(self.name) > 255:
            raise ValueError("Name cannot be longer than 255 characters")

        if self.type not in CastMemberType:
            raise ValueError("Cast member type must be DIRECTOR or ACTOR")


    def update_cast_member(self, name: str, type: CastMemberType):
        self.name = name
        self.type = type
        self.validate()

