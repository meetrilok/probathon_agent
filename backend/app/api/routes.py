from fastapi import APIRouter, Depends

from app.api.dependencies import get_use_case_service, get_validation_agent
from app.api.schemas import (
    DashboardResponse,
    RequiredInputDescriptor,
    RequiredInputsResponse,
    UseCaseCreateRequest,
    UseCaseResponse,
    ValidateIdeaRequest,
    ValidationResponse,
)
from app.domain.models import UseCase
from app.services.use_case_service import UseCaseService
from app.agents.validation_agent import ValidationAgent


router = APIRouter(prefix="/api", tags=["use-cases"])


@router.get("/required-inputs", response_model=RequiredInputsResponse)
def required_inputs() -> RequiredInputsResponse:
    return RequiredInputsResponse(
        ingestion=[
            RequiredInputDescriptor(key="title", label="Use case title", required=True, description="Unique name of use case"),
            RequiredInputDescriptor(key="description", label="Use case description", required=True, description="Detailed explanation"),
            RequiredInputDescriptor(key="lob", label="Line of business", required=True, description="LOB owner"),
            RequiredInputDescriptor(key="contact_email", label="Owner email", required=False, description="Partner contact"),
            RequiredInputDescriptor(key="source_uri", label="Source URI", required=False, description="Repo/API/Harness link"),
        ],
        validation=[
            RequiredInputDescriptor(key="idea_title", label="Idea title", required=True, description="Name of candidate idea"),
            RequiredInputDescriptor(key="idea_description", label="Idea description", required=True, description="Business objective and scope"),
            RequiredInputDescriptor(key="lob", label="Line of business", required=True, description="Candidate owner LOB"),
        ],
        infrastructure=[
            RequiredInputDescriptor(key="app_code_location", label="Application code location", required=True, description="Git repo or storage"),
            RequiredInputDescriptor(key="runtime_env", label="Runtime environment", required=True, description="Namespace/cluster/tenant"),
            RequiredInputDescriptor(key="existing_data_source", label="Existing DB", required=False, description="MongoDB, SQL, etc."),
        ],
    )


@router.post("/use-cases", response_model=UseCaseResponse)
def ingest_use_case(
    payload: UseCaseCreateRequest,
    service: UseCaseService = Depends(get_use_case_service),
) -> UseCaseResponse:
    use_case = UseCase(id=None, **payload.model_dump())
    created = service.ingest(use_case)
    return UseCaseResponse(**created.__dict__)


@router.get("/use-cases", response_model=list[UseCaseResponse])
def list_use_cases(service: UseCaseService = Depends(get_use_case_service)) -> list[UseCaseResponse]:
    return [UseCaseResponse(**item.__dict__) for item in service.list_use_cases()]


@router.post("/validate", response_model=ValidationResponse)
def validate_idea(
    payload: ValidateIdeaRequest,
    validator: ValidationAgent = Depends(get_validation_agent),
) -> ValidationResponse:
    result = validator.validate(payload.idea_title, payload.idea_description, payload.lob)
    return ValidationResponse(**result.__dict__)


@router.get("/dashboard", response_model=DashboardResponse)
def dashboard(service: UseCaseService = Depends(get_use_case_service)) -> DashboardResponse:
    snapshot = service.dashboard()
    recent = [UseCaseResponse(**item.__dict__) for item in snapshot["recent_use_cases"]]
    return DashboardResponse(total_use_cases=snapshot["total_use_cases"], by_lob=snapshot["by_lob"], recent_use_cases=recent)
