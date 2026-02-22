from collections import Counter

from app.domain.models import ValidationResult
from app.providers.embedding import EmbeddingProvider
from app.providers.vector_store import VectorStore
from app.repositories.base import UseCaseRepository


class ValidationAgent:
    def __init__(
        self,
        repository: UseCaseRepository,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        self.repository = repository
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    def validate(self, idea_title: str, idea_description: str, lob: str) -> ValidationResult:
        vector = self.embedding_provider.embed(f"{idea_title}\n{idea_description}\n{lob}")
        nearest = self.vector_store.search(vector, k=5)

        use_case_lookup = {use_case.id: use_case for use_case in self.repository.list_all()}
        nearest_use_cases: list[dict] = []
        for item_id, similarity in nearest:
            match = use_case_lookup.get(item_id)
            if not match:
                continue
            nearest_use_cases.append(
                {
                    "id": match.id,
                    "title": match.title,
                    "lob": match.lob,
                    "similarity": round(similarity, 4),
                    "contact_email": match.contact_email,
                }
            )

        in_lob_match = any(match["lob"].lower() == lob.lower() for match in nearest_use_cases)
        recommended_partner_contact = None
        for match in nearest_use_cases:
            if match["lob"].lower() == lob.lower() and match["contact_email"]:
                recommended_partner_contact = match["contact_email"]
                break

        semantic_group = self._semantic_group(nearest_use_cases)
        return ValidationResult(
            idea_title=idea_title,
            nearest_use_cases=nearest_use_cases,
            in_lob_match=in_lob_match,
            recommended_partner_contact=recommended_partner_contact,
            semantic_group=semantic_group,
        )

    @staticmethod
    def _semantic_group(nearest_use_cases: list[dict]) -> str:
        if not nearest_use_cases:
            return "net-new"
        most_common_lob = Counter(item["lob"] for item in nearest_use_cases).most_common(1)[0][0]
        return f"cluster:{most_common_lob.lower().replace(' ', '-')}"
