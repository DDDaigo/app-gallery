# backend/app/routers/projects.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..db import get_db
from ..models import Project
from ..schemas import ProjectOut, ProjectCreate, ProjectUpdate
from ..deps import require_admin

router = APIRouter(prefix="/projects", tags=["projects"])

# --- helpers ---
def _list_to_csv(v: list[str]) -> str:
    return ",".join([x.strip() for x in (v or []) if x.strip()])

# --- admin ---
@router.get("/admin/ping")
def admin_ping(_: bool = Depends(require_admin)):
    return {"ok": True}

@router.get(
    "/admin/all",
    response_model=List[ProjectOut],
    dependencies=[Depends(require_admin)],
)
def admin_list_all(db: Session = Depends(get_db)):
    rows = db.query(Project).order_by(Project.created_at.desc()).all()
    return [ProjectOut.model_validate(r) for r in rows]

# --- public ---
@router.get("/", response_model=List[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None),
    sort: str = Query("new"),
):
    stmt = db.query(Project).filter(Project.is_published.is_(True))
    if q:
        like = f"%{q}%"
        stmt = stmt.filter(Project.title.ilike(like) | Project.description.ilike(like))
    if sort == "new":
        stmt = stmt.order_by(Project.created_at.desc())
    rows = stmt.all()
    # ProjectOut 側の @computed_field が tags_csv→tags[] を作るので、素直に返せばOK
    return [ProjectOut.model_validate(r) for r in rows]

@router.get("/{slug}", response_model=ProjectOut)
def get_project(slug: str, db: Session = Depends(get_db)):
    proj = db.query(Project).filter(Project.slug == slug).first()
    if not proj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    return ProjectOut.model_validate(proj)

# --- create/update/delete (admin) ---
@router.post(
    "/", response_model=ProjectOut, dependencies=[Depends(require_admin)]
)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    # slug 重複チェック
    if db.query(Project).filter_by(slug=payload.slug).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "slug already exists")

    proj = Project(
        title=payload.title,
        slug=payload.slug,
        description=payload.description,
        image_url=payload.image_url or "",
        repo_url=payload.repo_url or "",
        app_url=payload.app_url or "",
        tech_stack=payload.tech_stack or "",
        story_md=payload.story_md or "",
        tags_csv=_list_to_csv(payload.tags),
        is_published=payload.is_published,
    )
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return ProjectOut.model_validate(proj)

@router.put(
    "/{project_id}",
    response_model=ProjectOut,
    dependencies=[Depends(require_admin)],
)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    proj = db.get(Project, project_id)
    if not proj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")

    data = payload.dict(exclude_unset=True)

    # slug を変更するなら一意性チェック
    new_slug = data.get("slug")
    if new_slug and new_slug != proj.slug:
        exists = db.query(Project).filter(Project.slug == new_slug, Project.id != project_id).first()
        if exists:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "slug already exists")

    # tags[] を受け取ったときのみ CSV へ
    if "tags" in data and data["tags"] is not None:
        proj.tags_csv = _list_to_csv(data.pop("tags") or [])

    for k, v in data.items():
        setattr(proj, k, v)

    db.add(proj)
    db.commit()
    db.refresh(proj)
    return ProjectOut.model_validate(proj)

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    proj = db.get(Project, project_id)
    if not proj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    db.delete(proj)
    db.commit()
