from typing import Optional

from app.models.research import Publication
from app.repositories.publication import PublicationRepository


class PublicationService:
    def __init__(self, publication_repo: PublicationRepository):
        self.publication_repo = publication_repo

    def submit_for_review(
        self,
        *,
        title: str,
        abstract: str,
        researcher_id: int,
        pdf_path: str,
        doi: str | None = None,
        keywords: list[str] | None = None,
        year: int | None = None,
    ) -> Publication:
        return self.publication_repo.create_submission(
            title=title,
            abstract=abstract,
            researcher_id=researcher_id,
            pdf_path=pdf_path,
            doi=doi,
            keywords=keywords,
            year=year,
        )

    def search_approved(self, query: str) -> list[Publication]:
        # STUDENT SNIPPET: complete the service behavior for publication search.
        return self.publication_repo.search_approved(query)

    def get_approved(self, pub_id: int) -> Optional[Publication]:
        # Delegate the lookup to the repository
        return self.publication_repo.get_approved(pub_id)

    def list_citations(self, pub_id: int) -> list[Publication]:
        # Delegate the citation list retrieval to the repository
        return self.publication_repo.list_citations(pub_id)

    def list_references(self, pub_id: int) -> list[Publication]:
        # Delegate the reference list retrieval to the repository
        return self.publication_repo.list_references(pub_id)

    def list_for_researcher(self, user_id: int) -> list[Publication]:
        # Delegate the researcher submissions retrieval to the repository
        return self.publication_repo.list_for_researcher(user_id)