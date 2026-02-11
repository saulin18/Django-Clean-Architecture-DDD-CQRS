import factory
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from src.quotes.models import Quote, Subquote

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    password = factory.Faker("password")


class QuoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quote

    user = factory.SubFactory(UserFactory)
    text = factory.Faker("sentence")


class SubquoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subquote

    quote = factory.SubFactory(QuoteFactory)
    text = factory.Faker("sentence")


class SubquotePayloadFactory(factory.DictFactory):
    text = factory.Faker("sentence")


class CreateQuotePayloadFactory(factory.DictFactory):
    text = factory.Faker("sentence")
    subquotes = factory.LazyFunction(lambda: [SubquotePayloadFactory()])


class CreateQuoteWithSubquotesPayloadFactory(factory.DictFactory):
    text = factory.Faker("sentence")
    subquotes = factory.List(
        [
            factory.SubFactory(SubquotePayloadFactory),
            factory.SubFactory(SubquotePayloadFactory),
        ],
    )
    user_id = factory.Faker("pyint")


@pytest.mark.integration
@pytest.mark.django_db
def test_list_quotes_empty(api_client):
    response = api_client.get("/api/quotes/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.integration
@pytest.mark.django_db
def test_create_quote_with_subquotes(api_client: APIClient):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    payload = CreateQuoteWithSubquotesPayloadFactory()
    response = api_client.post("/api/quotes/", payload, format="json")
    assert response.status_code == 201
