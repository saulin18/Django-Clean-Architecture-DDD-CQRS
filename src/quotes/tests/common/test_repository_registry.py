import pytest

from src.common.repository_registry import BaseRepository, RepositoryRegistry


@pytest.fixture(scope="function", autouse=True)
def teardown_function():
    import src.common.repository_registry as m

    m.RepositoryRegistry._instance = None


@pytest.fixture(scope="function")
def repository_registry():
    return RepositoryRegistry()


def test_repository_registry_must_be_a_singleton(repository_registry):

    first_registry = repository_registry
    assert first_registry is not None

    with pytest.raises(Exception):
        # Try to create a new instance of the RepositoryRegistry
        RepositoryRegistry()


def test_register_and_get_repository_from_registry(repository_registry):

    registry = repository_registry
    assert registry is not None

    class FakeRepository(BaseRepository):
        def __init__(self, repository_registry: RepositoryRegistry):
            super().__init__("fake", repository_registry)

    fake_repository = FakeRepository(registry)
    assert fake_repository is not None
    assert registry.get("fake") is not None
    assert registry.get("fake") == fake_repository
