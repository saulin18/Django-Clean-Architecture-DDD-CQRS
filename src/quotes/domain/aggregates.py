from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID, uuid4

from src.quotes.domain.entities import Subquote


class Quote:
    def __init__(
        self,
        user_id: int,
        text: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        subquotes: List[Subquote] | None = None,
        id: UUID | None = None,
    ) -> None:
        self.id = id or uuid4()
        self.user_id = user_id
        self.text = text
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.subquotes: List[Subquote] = subquotes or []

    def add_subquote(self, subquotes: List[Dict[str, Any]]) -> "Quote":
        for subquote in subquotes:
            sub = Subquote(quote_id=self.id, text=subquote.get("text", ""))
            self.subquotes.append(sub)
        return self

    def __str__(self) -> str:
        return f"Quote(id={self.id}, user_id={self.user_id}, text={self.text}, created_at={self.created_at})"

    def __repr__(self) -> str:
        return self.__str__()
