from typing import Optional

from app.models.research import Publication
from app.repositories.review import ReviewRepository


class ReviewService:
    def __init__(self, review_repo: ReviewRepository):
        self.review_repo = review_repo

    def list_pending(self) -> list[Publication]:
        # STUDENT SNIPPET: complete the pending-review service behavior.
        return self.review_repo.list_pending()

    def get_pending(self, pub_id: int) -> Optional[Publication]:
        # STUDENT SNIPPET: complete the selected-paper service behavior.
        return self.review_repo.get_pending(pub_id)

    def decide(self, pub_id: int, admin_user_id: int, decision: str) -> bool:
        # STUDENT SNIPPET: validate the decision and delegate persistence.
        if decision not in ["approve", "reject"]:
            raise ValueError("Invalid decision. Must be 'approve' or 'reject'.")
        return self.review_repo.save_decision(pub_id, admin_user_id, decision)