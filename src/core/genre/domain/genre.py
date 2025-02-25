from dataclasses import dataclass, field
from typing import Set
from uuid import UUID

from src.core._shared.entity import AbstractEntity


@dataclass(kw_only=True)
class Genre(AbstractEntity):
    name: str
    is_active: bool = True
    categories: set[UUID] = field(default_factory=set)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            self.notification.add_error("name must have less than 256 characters")
            # raise ValueError("")

        if len(self.name) == 0:
            self.notification.add_error("name cannot be empty")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def change_name(self, name):
        self.name = name
        self.validate()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def add_category(self, category_id: UUID):
        self.categories.add(category_id)
        self.validate()

    def remove_category(self, category_id: UUID):
        self.categories.remove(category_id)
        self.validate()

    def update_categories(self, category_ids: Set[UUID]) -> None:
        self.categories = category_ids
        self.validate()