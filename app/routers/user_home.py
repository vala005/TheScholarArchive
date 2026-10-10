from pathlib import Path
import time

from fastapi import File, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
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

    if user.role != "researcher":
        saved_papers = service.list_saved_publications(user.id)
        return templates.TemplateResponse(
            request=request,
            name="reader-home.html",
            context={
                "user": user,
                "saved_papers": saved_papers,
            },
        )

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
    authors: str = Form(...),
    year: int | None = Form(default=None),
    file: UploadFile = File(...),
):
    if user.role != "researcher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only researcher accounts can submit papers.",
        )
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to identify the signed-in researcher.",
        )

    repo = PublicationRepository(db)
    service = PublicationService(repo)
    try:
        author_list = service.parse_author_names(authors)
    except ValueError as exc:
        flash(request, str(exc), "danger")
        return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        flash(request, "Please upload a PDF file for review.", "danger")
        return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)

    researcher = service.get_or_create_researcher(
        user_id=user.id,
        username=user.username,
    )

    if researcher.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to identify the researcher profile.",
        )

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
    # Bind author names from the form and pass them to the service; persistence
    # stays in the repository.
    service.submit_for_review(
        title=title.strip(),
        abstract=abstract.strip(),
        researcher_id=researcher.id,
        pdf_path=safe_name,
        doi=doi.strip() if doi else None,
        keywords=keyword_list,
        authors=author_list,
        year=year,
    )

    flash(request, "Paper submitted for review.")
    return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)