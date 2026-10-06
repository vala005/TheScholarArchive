from pathlib import Path

from fastapi import HTTPException, Request, status
from fastapi.responses import FileResponse, HTMLResponse

from app.dependencies.auth import AuthDep, IsUserLoggedIn
from app.dependencies.session import SessionDep
from app.repositories.publication import PublicationRepository
from app.services.publication_service import PublicationService

from . import router, templates

PDF_STORAGE_ROOT = Path("storage/pdfs").resolve()


@router.get("/publications", response_class=HTMLResponse, name="publications_view")
async def publications_view(
    request: Request,
    user_logged_in: IsUserLoggedIn,
    db: SessionDep,
    q: str | None = "",
):
    repository = PublicationRepository(db)
    service = PublicationService(repository)
    publications = service.search_approved(q or "")
    return templates.TemplateResponse(
        request=request,
        name="publications.html",
        context={
            "query": q,
            "publications": publications,
            "user_logged_in": user_logged_in,
        },
    )


@router.get("/publications/{pub_id}", response_class=HTMLResponse, name="publication_detail_view")
async def publication_detail_view(
    pub_id: int,
    request: Request,
    user: AuthDep,
    db: SessionDep,
):
    repository = PublicationRepository(db)
    service = PublicationService(repository)

    paper = service.get_approved(pub_id)
    if paper is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Publication not found.")

    citations = service.list_citations(pub_id)
    references = service.list_references(pub_id)

    return templates.TemplateResponse(
        request=request,
        name="publication-detail.html",
        context={
            "paper": paper,
            "citations": citations,
            "references": references,
            "user": user,
        },
    )


@router.get("/publications/{pub_id}/pdf", name="publication_pdf_view")
async def publication_pdf_view(
    pub_id: int,
    user: AuthDep,
    db: SessionDep,
):
    repository = PublicationRepository(db)
    service = PublicationService(repository)

    paper = service.get_approved(pub_id)
    if paper is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Publication not found.")

    if not paper.pdf_path:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No PDF available for this publication.")

    candidate = (PDF_STORAGE_ROOT / paper.pdf_path).resolve()
    if not candidate.is_relative_to(PDF_STORAGE_ROOT) or not candidate.is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "PDF file missing.")

    return FileResponse(
        path=candidate,
        media_type="application/pdf",
        filename=f"{paper.id}.pdf",
        content_disposition_type="inline",
    )