from typing import List, Optional
from uuid import UUID

from src.common.repository_registry import RepositoryRegistry
from src.quotes.adapters.orm import BadgeModel, QuoteModel, SubquoteModel
from src.quotes.domain.aggregates import Quote
from src.quotes.domain.entities import Badge, Subquote
from src.quotes.interfaces.repositories import BadgeRepository, QuoteRepository


def _subquote_to_domain(s: SubquoteModel) -> Subquote:
    return Subquote(
        id=s.id,
        quote_id=s.quote_id,
        text=s.text,
        created_at=s.created_at,
        updated_at=getattr(s, "updated_at", s.created_at),
    )


class DjangoQuoteRepository(QuoteRepository):
    def __init__(self, repository_registry: RepositoryRegistry):
        super().__init__("quotes", repository_registry)

    def list(self) -> List[Quote]:
        quotes = QuoteModel.objects.prefetch_related("subquotes").all()
        return [self.to_domain(quote) for quote in quotes]

    def to_domain(self, quote: QuoteModel) -> Quote:
        subquotes = [_subquote_to_domain(s) for s in quote.subquotes.all()]
        return Quote(
            id=quote.id,
            user_id=quote.user.id,
            text=quote.text,
            created_at=quote.created_at,
            updated_at=quote.updated_at,
            subquotes=subquotes,
        )

    def create(self, quote: Quote) -> None:
        created = QuoteModel.objects.create(
            id=quote.id,
            user_id=quote.user_id,
            text=quote.text,
        )

        SubquoteModel.objects.bulk_create(
            [
                SubquoteModel(id=sub.id, quote_id=created.id, text=sub.text)
                for sub in quote.subquotes
            ]
        )

    def get(self, id: UUID) -> Optional[Quote]:
        try:
            quote = QuoteModel.objects.prefetch_related("subquotes").get(id=id)
            return self.to_domain(quote)
        except QuoteModel.DoesNotExist:
            return None

    def update(self, quote: Quote) -> None:
        QuoteModel.objects.filter(id=quote.id).update(
            text=quote.text,
            updated_at=quote.updated_at,
        )

        sub_ids = {s.id: s for s in quote.subquotes if s.id}

        SubquoteModel.objects.filter(quote_id=quote.id).exclude(
            id__in=sub_ids.keys()
        ).delete()

        existent_subquotes = SubquoteModel.objects.filter(quote_id=quote.id)
        existent_subquotes_ids = existent_subquotes.values_list("id", flat=True)

        to_update = [s for s in quote.subquotes if s.id in existent_subquotes_ids]
        to_create = [s for s in quote.subquotes if s.id not in existent_subquotes_ids]

        if to_update:
            text_by_id = {
                s.id: (s.text, getattr(s, "updated_at", None)) for s in to_update
            }
            objs = list(existent_subquotes)
            for obj in objs:
                obj.text, obj.updated_at = (
                    text_by_id[obj.id][0],
                    text_by_id[obj.id][1] or obj.updated_at,
                )
            SubquoteModel.objects.bulk_update(objs, ["text", "updated_at"])

        if to_create:
            SubquoteModel.objects.bulk_create(
                [
                    SubquoteModel(id=s.id, quote_id=quote.id, text=s.text)
                    for s in to_create
                ]
            )


class DjangoBadgeRepository(BadgeRepository):
    def __init__(self, repository_registry: RepositoryRegistry):
        super().__init__("badges", repository_registry)

    def to_domain(self, badge: BadgeModel) -> Badge:
        return Badge(
            id=badge.id,
            name=badge.name,
            description=badge.description,
            quote_id=badge.quote_id,
            created_at=badge.created_at,
        )

    def get(self, id: int) -> Optional[Badge]:
        try:
            badge = BadgeModel.objects.get(id=id)
            return self.to_domain(badge)
        except BadgeModel.DoesNotExist:
            return None

    def create(self, badge: Badge) -> None:
        BadgeModel.objects.create(
            name=badge.name,
            description=badge.description,
            quote_id=badge.quote_id,
        )

    def update(self, badge: Badge) -> None:
        BadgeModel.objects.filter(id=badge.id).update(
            name=badge.name,
            description=badge.description,
            quote_id=badge.quote_id,
        )

    def delete(self, id: int) -> None:
        BadgeModel.objects.filter(id=id).delete()
