from __future__ import annotations

from typing import Iterator, Self

from loguru import logger


class RepositoryRegistry:
    """
    This class is used to register automatically each instance of the BaseRepository class.
    """

    _instance = None

    def __new__(cls) -> Self:
        if RepositoryRegistry._instance is not None:
            logger.error("RepositoryRegistry is a singleton")
            raise Exception("RepositoryRegistry is a singleton")
        instance = super().__new__(cls)
        instance.repositories = {}
        RepositoryRegistry._instance = instance
        return instance

    def __str__(self) -> str:
        return f"RepositoryRegistry(repositories={self.repositories})"

    def __repr__(self) -> str:
        return self.__str__()

    def register(self, name: str, repository: "BaseRepository") -> None:
        self.repositories[name] = repository

    def get(self, name: str) -> "BaseRepository" | None:
        return self.repositories.get(name, None)

    def __iter__(self) -> Iterator["BaseRepository"]:
        return iter(self.repositories.values())


class BaseRepository:
    """
    Base class for all repositories.
    This class is used to create a new instance of the BaseRepository class and register it in the RepositoryRegistry.
    Before creating any repository, you must create the RepositoryRegistry instance.
    """

    def __init__(self, name: str, repository_registry: RepositoryRegistry):
        self.name = name
        self.repository_registry = repository_registry

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        if instance.repository_registry is not None:
            instance.repository_registry.register(instance.name, instance)

        return instance
