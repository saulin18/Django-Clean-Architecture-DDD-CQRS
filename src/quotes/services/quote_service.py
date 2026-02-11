from typing import List
from uuid import UUID

from src.common.uow import UnitOfWork
from src.quotes.domain.aggregates import Quote
from src.quotes.interfaces.repositories import BadgeRepository, QuoteRepository


class QuoteService:
    def __init__(
        self,
        uow: UnitOfWork,
        quote_repository: QuoteRepository,
        badge_repository: BadgeRepository,
    ):
        self.uow = uow
        self.quote_repository = quote_repository
        self.badge_repository = badge_repository

    def create_quote(self, quote: Quote) -> None:
        with self.uow:
            existent_quote = self.quote_repository.get(quote.id)

            if existent_quote:
                raise ValueError(
                    f"The quote {existent_quote.text, existent_quote.id} already exists"
                )

            self.quote_repository.create(quote)

    def update_quote(self, quote: Quote) -> None:
        with self.uow:
            existent_quote = self.quote_repository.get(quote.id)

            if not existent_quote:
                raise ValueError(f"The quote {quote.text, quote.id} does not exist")

            self.quote_repository.update(quote)

    def get_all_quotes(self) -> List[Quote]:
        with self.uow:
            quotes = self.quote_repository.list()
            return quotes

    def get_quote_by_id(self, id: UUID) -> Quote | None:
        with self.uow:
            quote = self.quote_repository.get(id)
            return quote
