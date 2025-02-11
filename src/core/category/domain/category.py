from dataclasses import dataclass

from src.core._shared.entity import AbstractEntity


@dataclass(kw_only=True)
class Category(AbstractEntity):
    name: str
    description: str = ""
    is_active: bool = True

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            self.notification.add_error("name must have less than 256 characters")

        if len(self.name) == 0:
            self.notification.add_error("name cannot be empty")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def update_category(self, name, description):
        self.name = name
        self.description = description
        self.validate()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
