from app.domain.models import UseCase
from app.providers.embedding import EmbeddingProvider
from app.providers.vector_store import VectorStore
from app.repositories.base import UseCaseRepository


class UseCaseService:
    def __init__(
        self,
        repository: UseCaseRepository,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        self.repository = repository
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    def ingest(self, use_case: UseCase) -> UseCase:
        persisted = self.repository.create(use_case)
        vector = self.embedding_provider.embed(f"{persisted.title}\n{persisted.description}\n{persisted.lob}")
        self.vector_store.add(persisted.id or -1, vector)
        return persisted

    def list_use_cases(self) -> list[UseCase]:
        return self.repository.list_all()

    def dashboard(self) -> dict:
        all_items = self.repository.list_all()
        by_lob = self.repository.count_by_lob()
        return {
            "total_use_cases": len(all_items),
            "by_lob": by_lob,
            "recent_use_cases": all_items[:10],
        }
