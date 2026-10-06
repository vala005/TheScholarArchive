from typing import Optional

from sqlmodel import Session

from app.models.research import Publication, Review, Admin

class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_pending(self) -> list[Publication]:
    # STUDENT SNIPPET: retrieve publications awaiting an admin decision.
        return (
            self.db.query(Publication)
            .filter(Publication.status == "under review")
            .all()
        )

    def get_pending(self, pub_id: int) -> Optional[Publication]:
        # STUDENT SNIPPET: retrieve one pending publication by id.
        return self.db.query(Publication).filter(Publication.id == pub_id, Publication.status == "under review").first()

    def save_decision(
        self,
        pub_id: int,
        reviewer_id: int,
        decision: str,
        comments: str = "",
    ) -> bool:
            # STUDENT SNIPPET: persist the Review and update Publication status.
            publication = self.db.query(Publication).filter(Publication.id == pub_id).first()
            if not publication:
                return False

            # Resolve the Admin profile for the given user id
            admin = self.db.query(Admin).filter(Admin.user_id == reviewer_id).first()
            if not admin:
                return False

            # Map decision -> new publication status
            new_status = "approved" if decision == "approve" else "rejected"

            # Create the Review record
            review = Review(
                pub_id=pub_id,
                reviewer_id=admin.id,
                decision=decision,
                comments=comments,
            )
            self.db.add(review)

            # Update the publication status
            publication.status = new_status
            self.db.add(publication)

            self.db.commit()
            return True
    