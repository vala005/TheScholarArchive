from typing import Optional

from sqlmodel import Session, select

from app.models.research import Citation, Publication, Researcher, SavedPublication


class PublicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_submission(
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
        publication = Publication(
            title=title,
            abstract=abstract,
            status="under review",
            researcher_id=researcher_id,
            doi=doi.strip() if doi and doi.strip() else None,
            keywords=keywords or [],
            year=year,
            pdf_path=pdf_path,
        )
        self.db.add(publication)
        self.db.commit()
        self.db.refresh(publication)
        return publication

    def search_approved(self, query: str | None) -> list[Publication]:
        # Accept blank/null input as a full archive listing and match against the
        # user-visible paper fields that matter to a reader search.
        normalized = (query or "").strip()
        base = self.db.query(Publication).filter(Publication.status == "approved")

        if not normalized:
            return base.all()

        term = f"%{normalized}%"
        return base.filter(
            (Publication.title.ilike(term))
            | (Publication.abstract.ilike(term))
            | (Publication.doi.ilike(term))
        ).all()

    def get_approved(self, pub_id: int) -> Optional[Publication]:
        # STUDENT SNIPPET: return one approved publication by id.
        return self.db.query(Publication).filter(
            Publication.id == pub_id,
            Publication.status == "approved"
        ).first()
    
    def list_citations(self, pub_id: int) -> list[Publication]:
        # STUDENT SNIPPET: return approved publications that cite this paper.
        return self.db.query(Publication).join(
            Citation, Citation.citing_pub_id == Publication.id
        ).filter(
            Citation.cited_pub_id == pub_id,
            Publication.status == "approved"
        ).all()

    def list_references(self, pub_id: int) -> list[Publication]:
        # STUDENT SNIPPET: return approved publications cited by this paper.
        return self.db.query(Publication).join(
            Citation, Citation.cited_pub_id == Publication.id
        ).filter(
            Citation.citing_pub_id == pub_id,
            Publication.status == "approved"
        ).all()

    def list_for_researcher(self, user_id: int) -> list[Publication]:
        # 1. Find the Researcher profile linked to this user_id
        researcher = self.db.exec(
            select(Researcher).where(Researcher.user_id == user_id)
        ).one_or_none()

        # 2. If no researcher profile exists, regular users should still be able to
        #    view the published archive instead of getting a blank dashboard.
        if researcher is None:
            return self.db.exec(
                select(Publication).where(Publication.status == "approved")
            ).all()

        # 3. Fetch all publications for this researcher, regardless of status
        publications = self.db.exec(
            select(Publication).where(Publication.researcher_id == researcher.id)
        ).all()

        return list(publications)

    def toggle_saved_publication(self, user_id: int, publication_id: int) -> bool:
        existing = self.db.exec(
            select(SavedPublication).where(
                SavedPublication.user_id == user_id,
                SavedPublication.publication_id == publication_id,
            )
        ).one_or_none()
        if existing is not None:
            self.db.delete(existing)
            self.db.commit()
            return False
        self.db.add(
            SavedPublication(user_id=user_id, publication_id=publication_id)
        )
        self.db.commit()
        return True

    def is_saved_publication(self, user_id: int, publication_id: int) -> bool:
        saved_id = self.db.exec(
            select(SavedPublication.id).where(
                SavedPublication.user_id == user_id,
                SavedPublication.publication_id == publication_id,
            )
        ).first()
        return saved_id is not None

    def list_saved_publications(self, user_id: int) -> list[Publication]:
        return self.db.exec(
            select(Publication)
            .join(SavedPublication, SavedPublication.publication_id == Publication.id)
            .where(
                SavedPublication.user_id == user_id,
                Publication.status == "approved",
            )
            .order_by(Publication.title)
        ).all()

    def list_saved_publication_ids(self, user_id: int) -> set[int]:
        return set(
            self.db.exec(
                select(SavedPublication.publication_id).where(
                    SavedPublication.user_id == user_id,
                )
            ).all()
        )