from dataclasses import dataclass

from src.config import DEFAULT_PER_PAGE_SIZE


@dataclass
class ListRequest:
    order_by: str = "name"
    current_page: int = 1
    per_page: int = DEFAULT_PER_PAGE_SIZE

@dataclass
class ListOutputMeta:
    current_page: int
    per_page: int
    total: int
