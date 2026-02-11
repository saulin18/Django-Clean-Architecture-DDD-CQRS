import logging

from django.db import transaction
from django.db.transaction import Atomic

from src.common.repository_registry import BaseRepository, RepositoryRegistry


class UnitOfWork:
    """
    UOW class for managing transactions between repositories within the same unit of work and registry

    Example:
    with UnitOfWork(repository_registry) as uow:
        repository = uow.get_repository("repository_name")
        repository.do_something()
    or
    with UnitOfWork(repository_registry) as uow:
        repository = uow.get_repository("repository_name")

     You can access the transaction and the registry directly from the instance, as well as registering and getting all repositories.
    """

    def __init__(self, repository_registry: RepositoryRegistry):
        self.transaction: Atomic = transaction.atomic()
        self.repository_registry = repository_registry

    def __enter__(self) -> "UnitOfWork":
        self.transaction.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            logging.error("Transaction rolled back")
            raise exc_value
        else:
            logging.info("Transaction committed")
        self.transaction.__exit__(exc_type, exc_value, traceback)

    def get_repository(self, name: str) -> BaseRepository | None:
        return self.repository_registry.get(name)

    def get_all_repositories(self) -> list[BaseRepository]:
        return list(self.repository_registry)

    def register_repository(self, name: str, repository: BaseRepository):
        self.repository_registry.register(name, repository)
