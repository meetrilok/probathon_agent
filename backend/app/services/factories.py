from sqlalchemy.orm import Session

from app.core.config import Settings
from app.providers.embedding import DeterministicHashEmbeddingProvider, EmbeddingProvider
from app.providers.vector_store import FaissVectorStore, VectorStore
from app.repositories.base import UseCaseRepository
from app.repositories.sqlite_use_case_repository import SqliteUseCaseRepository


class RepositoryFactory:
    @staticmethod
    def build_use_case_repository(settings: Settings, session: Session) -> UseCaseRepository:
        if settings.sql_db_url.startswith("sqlite"):
            return SqliteUseCaseRepository(session)
        raise ValueError(f"Unsupported SQL provider for URL: {settings.sql_db_url}")


class ProviderFactory:
    @staticmethod
    def build_embedding_provider(settings: Settings) -> EmbeddingProvider:
        if settings.embedding_provider == "deterministic":
            return DeterministicHashEmbeddingProvider(settings.vector_dimension)
        raise ValueError(f"Unsupported embedding provider: {settings.embedding_provider}")

    @staticmethod
    def build_vector_store(settings: Settings) -> VectorStore:
        if settings.vector_provider == "faiss":
            return FaissVectorStore(settings.vector_dimension, settings.vector_index_path)
        raise ValueError(f"Unsupported vector provider: {settings.vector_provider}")
