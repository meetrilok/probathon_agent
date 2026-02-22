from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class UseCase:
    id: int | None
    title: str
    description: str
    lob: str
    contact_email: str | None
    source_type: str
    source_uri: str | None
    created_at: datetime | None = None


@dataclass(slots=True)
class ValidationResult:
    idea_title: str
    nearest_use_cases: list[dict[str, Any]]
    in_lob_match: bool
    recommended_partner_contact: str | None
    semantic_group: str
