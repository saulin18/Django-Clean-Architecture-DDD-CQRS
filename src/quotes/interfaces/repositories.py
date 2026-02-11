from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.common.repository_registry import BaseRepository
from src.quotes.domain.aggregates import Quote
from src.quotes.domain.entities import Badge


class QuoteRepository(ABC, BaseRepository):
    @abstractmethod
    def list(self) -> List[Quote]:
        pass

    @abstractmethod
    def get(self, id: UUID) -> Optional[Quote]:
        pass

    @abstractmethod
    def create(self, quote: Quote) -> None:
        pass

    @abstractmethod
    def update(self, quote: Quote) -> None:
        pass


class BadgeRepository(ABC, BaseRepository):
    @abstractmethod
    def get(self, id: int) -> Optional[Badge]:
        pass

    @abstractmethod
    def create(self, badge: Badge) -> None:
        pass

    @abstractmethod
    def update(self, badge: Badge) -> None:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
