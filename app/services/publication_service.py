from typing import Optional

from app.models.research import Publication, Researcher
from app.repositories.publication import PublicationRepository


class PublicationService:
    def __init__(self, publication_repo: PublicationRepository):
        self.publication_repo = publication_repo

    def get_or_create_researcher(
        self,
        *,
        user_id: int,
        username: str,
    ) -> Researcher:
        return self.publication_repo.get_or_create_researcher(
            user_id=user_id,
            username=username,
        )

    def parse_author_names(self, authors_text: str) -> list[str]:
        authors = [name.strip() for name in authors_text.splitlines() if name.strip()]
        if not authors:
            raise ValueError("Enter at least one author name.")
        return authors

    def submit_for_review(
        self,
        *,
        title: str,
        abstract: str,
        researcher_id: int,
        pdf_path: str,
        authors: list[str],
        doi: str | None = None,
        keywords: list[str] | None = None,
        year: int | None = None,
    ) -> Publication:
        normalized_authors = [author.strip() for author in authors if author.strip()]
        if not normalized_authors:
            raise ValueError("At least one author name is required.")

        return self.publication_repo.create_submission(
            title=title,
            abstract=abstract,
            researcher_id=researcher_id,
            pdf_path=pdf_path,
            authors=normalized_authors,
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

    def toggle_saved_publication(self, user_id: int, publication_id: int) -> bool:
        if self.publication_repo.get_approved(publication_id) is None:
            return False

        return self.publication_repo.toggle_saved_publication(user_id, publication_id)

    def is_saved_publication(self, user_id: int, publication_id: int) -> bool:
        return self.publication_repo.is_saved_publication(user_id, publication_id)

    def list_saved_publications(self, user_id: int) -> list[Publication]:
        return self.publication_repo.list_saved_publications(user_id)

    def list_saved_publication_ids(self, user_id: int) -> set[int]:
        return self.publication_repo.list_saved_publication_ids(user_id)