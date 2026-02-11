import pytest

from src.common.repository_registry import BaseRepository, RepositoryRegistry
from src.common.uow import UnitOfWork


@pytest.fixture(scope="function", autouse=True)
def teardown_function():
    import src.common.repository_registry as m

    m.RepositoryRegistry._instance = None


@pytest.fixture(scope="function")
def repository_registry():
    return RepositoryRegistry()


@pytest.fixture(scope="function")
def uow(repository_registry):
    return UnitOfWork(repository_registry)


@pytest.mark.integration
@pytest.mark.django_db
def test_uow_works_as_a_context_manager(uow):
    with uow:
        assert uow.transaction is not None
        assert uow.repository_registry is not None

    assert uow.transaction is not None
    assert uow.repository_registry is not None


@pytest.mark.django_db
@pytest.mark.integration
def test_uow_can_commit(uow):
    with uow:
        assert uow.transaction is not None
        assert uow.repository_registry is not None


@pytest.mark.integration
@pytest.mark.django_db
def test_uow_can_rollback(uow):
    with uow:
        assert uow.transaction is not None
        assert uow.repository_registry is not None
        with pytest.raises(Exception):
            raise Exception("Test exception")


@pytest.mark.integration
@pytest.mark.django_db
def test_uow_enters_and_returns_itself(uow):
    with uow as uow_instance:
        assert uow_instance is uow
        assert uow_instance.transaction is not None
        assert uow_instance.repository_registry is not None


@pytest.mark.unit
@pytest.mark.django_db
def test_uow_can_get_repositories_from_the_registry(uow):
    class FakeRepository(BaseRepository):
        def __init__(self, repository_registry: RepositoryRegistry):
            super().__init__("fake", repository_registry)

    fake_repository = FakeRepository(uow.repository_registry)
    assert fake_repository is not None
    assert uow.get_repository("fake") is not None
    assert uow.get_repository("fake") == fake_repository
    assert len(uow.get_all_repositories()) == 1
