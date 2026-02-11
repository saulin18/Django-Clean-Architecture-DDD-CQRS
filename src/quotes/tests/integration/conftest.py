import pytest


@pytest.fixture(autouse=True)
def reset_singletons():
    import src.common.repository_registry as rr
    import src.quotes.ioc as ioc

    rr.RepositoryRegistry._instance = None
    ioc._container = None
