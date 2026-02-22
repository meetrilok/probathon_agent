from abc import ABC, abstractmethod

from app.domain.models import UseCase


class UseCaseRepository(ABC):
    @abstractmethod
    def create(self, use_case: UseCase) -> UseCase:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[UseCase]:
        raise NotImplementedError

    @abstractmethod
    def count_by_lob(self) -> dict[str, int]:
        raise NotImplementedError
