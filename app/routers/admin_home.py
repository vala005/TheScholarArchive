from fastapi import Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from app.dependencies.session import SessionDep
from app.dependencies.auth import AdminDep
from app.repositories.review import ReviewRepository
from app.services.review_service import ReviewService
from app.utilities.flash import flash
from . import router, templates


@router.get("/admin", response_class=HTMLResponse)
async def admin_home_view(
    request: Request,
    user: AdminDep,
    db: SessionDep,
):
    # STUDENT SNIPPET: fetch pending publications and render the review queue.
    repo = ReviewRepository(db)
    service = ReviewService(repo)
    papers = service.list_pending()

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "user": user,
            "papers": papers,
            "complete": False,
        },
    )


@router.get("/admin/papers/{pub_id}", response_class=HTMLResponse, name="review_paper_view")
async def review_paper_view(
    request: Request,
    pub_id: int,
    user: AdminDep,
    db: SessionDep,
):
    # STUDENT SNIPPET: fetch the selected pending paper and render its review screen.
    repo = ReviewRepository(db)
    service = ReviewService(repo)
    paper = service.get_pending(pub_id)

    if not paper:
        flash(request, "Paper not found or already reviewed.")
        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        request=request,
        name="review-paper.html",
        context={
            "user": user,
            "paper": paper,
        },
    )


@router.post("/admin/papers/{pub_id}/decision", name="review_decision_action")
async def review_decision_action(
    request: Request,
    pub_id: int,
    user: AdminDep,
    db: SessionDep,
    decision: str = Form(...),
):
    # STUDENT SNIPPET: pass the decision to the service and redirect to the queue.
    repo = ReviewRepository(db)
    service = ReviewService(repo)
    success = service.decide(pub_id, user.id, decision)

    if success:
        flash(request, "Review submitted successfully.")
    else:
        flash(request, "Unable to record decision. The paper may already be decided.")

    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    # await ReviewService.save_decision(db, pub_id, user.id, decision)
    # return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/admin/review-complete", response_class=HTMLResponse, include_in_schema=False)
async def review_complete_view(request: Request, user: AdminDep):
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "user": user,
            "papers": [],
            "complete": True,
        },
    )
