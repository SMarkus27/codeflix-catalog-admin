from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID, uuid4

from src.core._shared.entity import AbstractEntity


class CastMemberType(StrEnum):
    DIRECTOR = "DIRECTOR"
    ACTOR = "ACTOR"


@dataclass(kw_only=True)
class CastMember(AbstractEntity):
    name: str
    type: CastMemberType


    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) == 0:
            self.notification.add_error("Name cannot be empty")

        if len(self.name) > 255:
            self.notification.add_error("Name cannot be longer than 255 characters")

        if self.type not in CastMemberType:
            self.notification.add_error("Cast member type must be DIRECTOR or ACTOR")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def update_cast_member(self, name: str, type: CastMemberType):
        self.name = name
        self.type = type
        self.validate()

