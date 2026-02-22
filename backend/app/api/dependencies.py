from fastapi import Depends
from sqlalchemy.orm import Session

from app.agents.validation_agent import ValidationAgent
from app.core.config import get_settings
from app.db.session import get_session
from app.services.factories import ProviderFactory, RepositoryFactory
from app.services.use_case_service import UseCaseService


def get_use_case_service(session: Session = Depends(get_session)) -> UseCaseService:
    settings = get_settings()
    repository = RepositoryFactory.build_use_case_repository(settings, session)
    embedding_provider = ProviderFactory.build_embedding_provider(settings)
    vector_store = ProviderFactory.build_vector_store(settings)
    return UseCaseService(repository, embedding_provider, vector_store)


def get_validation_agent(session: Session = Depends(get_session)) -> ValidationAgent:
    settings = get_settings()
    repository = RepositoryFactory.build_use_case_repository(settings, session)
    embedding_provider = ProviderFactory.build_embedding_provider(settings)
    vector_store = ProviderFactory.build_vector_store(settings)
    return ValidationAgent(repository, embedding_provider, vector_store)
