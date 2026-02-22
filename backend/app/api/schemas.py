from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class UseCaseCreateRequest(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=8)
    lob: str = Field(min_length=2, max_length=120)
    contact_email: EmailStr | None = None
    source_type: str = Field(default="manual")
    source_uri: str | None = None


class UseCaseResponse(BaseModel):
    id: int
    title: str
    description: str
    lob: str
    contact_email: str | None
    source_type: str
    source_uri: str | None
    created_at: datetime


class ValidateIdeaRequest(BaseModel):
    idea_title: str = Field(min_length=3, max_length=200)
    idea_description: str = Field(min_length=8)
    lob: str = Field(min_length=2, max_length=120)


class ValidationResponse(BaseModel):
    idea_title: str
    nearest_use_cases: list[dict[str, Any]]
    in_lob_match: bool
    recommended_partner_contact: str | None
    semantic_group: str


class DashboardResponse(BaseModel):
    total_use_cases: int
    by_lob: dict[str, int]
    recent_use_cases: list[UseCaseResponse]


class RequiredInputDescriptor(BaseModel):
    key: str
    label: str
    required: bool
    description: str


class RequiredInputsResponse(BaseModel):
    ingestion: list[RequiredInputDescriptor]
    validation: list[RequiredInputDescriptor]
    infrastructure: list[RequiredInputDescriptor]
