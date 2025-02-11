from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.core._shared.notification import Notification


@dataclass
class AbstractEntity(ABC):

    id: UUID = field(default_factory=uuid4)
    notification: Notification = field(default_factory=Notification)

    @abstractmethod
    def validate(self):
        pass