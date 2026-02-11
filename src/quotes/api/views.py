from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from src.quotes.api.serializers import QuoteSerializer
from src.quotes.domain.aggregates import Quote
from src.quotes.domain.entities import Subquote
from src.quotes.ioc import get_container


def _to_uuid(pk: UUID | str) -> UUID:
    return pk if isinstance(pk, UUID) else UUID(str(pk))


class QuoteViewSet(viewsets.ViewSet):
    serializer_class = QuoteSerializer
    permission_classes = []

    def list(self, request: Request) -> Response:
        quotes = get_container().get_quote_service().get_all_quotes()
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        serializer = QuoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quote = Quote(
            user_id=request.user.id,
            text=serializer.validated_data.get("text"),
        )
        quote_with_subquotes = quote.add_subquote(
            serializer.validated_data.get("subquotes") or []
        )
        get_container().get_quote_service().create_quote(quote_with_subquotes)
        return Response(None, status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, pk: UUID | str) -> Response:
        quote = get_container().get_quote_service().get_quote_by_id(_to_uuid(pk))
        if quote is None:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        serializer = QuoteSerializer(quote)
        return Response(serializer.data)

    def update(self, request: Request, pk: UUID | str) -> Response:
        quote_id = _to_uuid(pk)
        quote = get_container().get_quote_service().get_quote_by_id(quote_id)
        if quote is None:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        serializer = QuoteSerializer(quote, data=request.data)
        serializer.is_valid(raise_exception=True)
        subquotes_data = serializer.validated_data.get("subquotes") or []
        quote = Quote(
            id=quote_id,
            user_id=serializer.validated_data.get("user_id"),
            text=serializer.validated_data.get("text"),
            created_at=serializer.validated_data.get("created_at"),
            updated_at=serializer.validated_data.get("updated_at"),
            subquotes=[
                Subquote(quote_id=quote_id, text=subquote.get("text", ""))
                for subquote in subquotes_data
            ],
        )
        get_container().get_quote_service().update_quote(quote)
        return Response(None, status=status.HTTP_200_OK)
