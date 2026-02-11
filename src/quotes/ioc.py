from src.common.repository_registry import RepositoryRegistry
from src.common.uow import UnitOfWork
from src.quotes.interfaces.repositories import BadgeRepository, QuoteRepository
from src.quotes.repositories.quote_repository import (
    DjangoBadgeRepository,
    DjangoQuoteRepository,
)
from src.quotes.services.quote_service import QuoteService


class QuotesContainer:
    def __init__(self) -> None:
        self.repository_registry = RepositoryRegistry()
        self.uow = UnitOfWork(self.repository_registry)
        self.quote_repository = DjangoQuoteRepository(self.repository_registry)
        self.badge_repository = DjangoBadgeRepository(self.repository_registry)
        self.quote_service = QuoteService(
            self.uow, self.quote_repository, self.badge_repository
        )

    def get_quote_service(self) -> QuoteService:
        return self.quote_service

    def get_quote_repository(self) -> QuoteRepository:
        return self.quote_repository

    def get_badge_repository(self) -> BadgeRepository:
        return self.badge_repository


_container: QuotesContainer | None = None


def get_container() -> QuotesContainer:
    global _container
    if _container is None:
        _container = QuotesContainer()
    return _container
