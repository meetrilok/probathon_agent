from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.sql_models import UseCaseORM
from app.domain.models import UseCase
from app.repositories.base import UseCaseRepository


class SqliteUseCaseRepository(UseCaseRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, use_case: UseCase) -> UseCase:
        record = UseCaseORM(
            title=use_case.title,
            description=use_case.description,
            lob=use_case.lob,
            contact_email=use_case.contact_email,
            source_type=use_case.source_type,
            source_uri=use_case.source_uri,
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return self._to_domain(record)

    def list_all(self) -> list[UseCase]:
        rows = self.session.execute(select(UseCaseORM).order_by(UseCaseORM.created_at.desc())).scalars().all()
        return [self._to_domain(row) for row in rows]

    def count_by_lob(self) -> dict[str, int]:
        use_cases = self.list_all()
        return dict(Counter(item.lob for item in use_cases))

    @staticmethod
    def _to_domain(row: UseCaseORM) -> UseCase:
        return UseCase(
            id=row.id,
            title=row.title,
            description=row.description,
            lob=row.lob,
            contact_email=row.contact_email,
            source_type=row.source_type,
            source_uri=row.source_uri,
            created_at=row.created_at,
        )
