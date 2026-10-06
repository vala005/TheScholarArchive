"""Database table models.

Import every table model here so ``SQLModel.metadata.create_all`` sees them.
"""

from app.models.user import User
from app.models.research import Admin, Citation, Publication, Researcher, Review

__all__ = ["Admin", "Citation", "Publication", "Researcher", "Review", "User"]
