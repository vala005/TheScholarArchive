from typing import Optional

from sqlalchemy import CheckConstraint, Column, JSON, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

from app.models.user import User


class Researcher(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True, index=True)
    first_name: str
    last_name: str
    affiliation: Optional[str] = None
    bio: Optional[str] = None
    user: User = Relationship(back_populates="researcher")
    publications: list["Publication"] = Relationship(back_populates="researcher")


class Admin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True, index=True)
    user: User = Relationship(back_populates="admin")
    reviews: list["Review"] = Relationship(back_populates="reviewer")
    publications: list["Publication"] = Relationship(back_populates="publisher")


class Publication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    abstract: str
    status: str
    researcher_id: int = Field(foreign_key="researcher.id", index=True)
    doi: Optional[str] = Field(default=None, unique=True)
    keywords: list[str] = Field(default_factory=list, sa_column=Column(JSON, nullable=False))
    authors: list[str] = Field(sa_column=Column(JSON, nullable=False))
    year: Optional[int] = None
    publisher_id: Optional[int] = Field(default=None, foreign_key="admin.id", index=True)
    # STUDENT SNIPPET: add an optional field for the stored PDF path here.
    pdf_path: Optional[str] = None
    researcher: Researcher = Relationship(back_populates="publications")
    publisher: Optional[Admin] = Relationship(back_populates="publications")
    reviews: list["Review"] = Relationship(back_populates="publication")


class Citation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    citing_pub_id: int = Field(foreign_key="publication.id", index=True)
    cited_pub_id: int = Field(foreign_key="publication.id", index=True)


class SavedPublication(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "publication_id",
            name="uq_saved_publication_user_paper",
        ),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    publication_id: int = Field(foreign_key="publication.id", index=True)


class Review(SQLModel, table=True):
    __table_args__ = (CheckConstraint("decision IN ('approve', 'reject')"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    pub_id: int = Field(foreign_key="publication.id", index=True)
    reviewer_id: int = Field(foreign_key="admin.id", index=True)
    decision: str
    comments: str
    reviewer: Admin = Relationship(back_populates="reviews")
    publication: Publication = Relationship(back_populates="reviews")
