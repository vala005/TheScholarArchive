from pathlib import Path
import time

from fastapi import File, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import select

from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
from app.models.research import Researcher
from app.repositories.publication import PublicationRepository
from app.services.publication_service import PublicationService
from app.utilities.flash import flash
from . import router, templates


@router.get("/app", response_class=HTMLResponse)
async def user_home_view(
    request: Request,
    user: AuthDep,
    db: SessionDep
):
    repo = PublicationRepository(db)
    service = PublicationService(repo)
    papers = service.list_for_researcher(user.id)

    return templates.TemplateResponse(
        request=request,
        name="app.html",
        context={
            "user": user,
            "papers": papers,
        }
    )


@router.post("/app/upload", name="submit_publication_action")
async def submit_publication_action(
    request: Request,
    user: AuthDep,
    db: SessionDep,
    title: str = Form(...),
    abstract: str = Form(...),
    doi: str | None = Form(default=None),
    keywords: str = Form(default=""),
    year: int | None = Form(default=None),
    file: UploadFile = File(...),
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        flash(request, "Please upload a PDF file for review.", "danger")
        return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)

    researcher = db.exec(select(Researcher).where(Researcher.user_id == user.id)).one_or_none()
    if researcher is None:
        researcher = Researcher(
            user_id=user.id,
            first_name=user.username,
            last_name="Researcher",
            affiliation="Independent",
            bio="Submitted through the archive upload workflow.",
        )
        db.add(researcher)
        db.commit()
        db.refresh(researcher)

    file_bytes = await file.read()
    if not file_bytes:
        flash(request, "The uploaded PDF is empty.", "danger")
        return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)

    storage_root = Path("storage/pdfs").resolve()
    storage_root.mkdir(parents=True, exist_ok=True)
    safe_name = f"{user.id}_{int(time.time())}_{Path(file.filename).name}"
    file_path = storage_root / safe_name
    file_path.write_bytes(file_bytes)

    keyword_list = [item.strip() for item in keywords.split(",") if item.strip()]
    repo = PublicationRepository(db)
    service = PublicationService(repo)
    service.submit_for_review(
        title=title.strip(),
        abstract=abstract.strip(),
        researcher_id=researcher.id,
        pdf_path=safe_name,
        doi=doi.strip() if doi else None,
        keywords=keyword_list,
        year=year,
    )

    flash(request, "Paper submitted for review.")
    return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)
