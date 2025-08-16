# backend/app/schemas.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, computed_field

class ProjectBase(BaseModel):
    title: str
    slug: str
    description: str
    image_url: Optional[str] = ""
    repo_url: Optional[str] = ""
    app_url: Optional[str] = ""
    tech_stack: Optional[str] = "Vue3, Tailwind, FastAPI"
    story_md: Optional[str] = ""
    is_published: bool = True

class ProjectCreate(ProjectBase):
    # API 入力は配列で受ける（DB では CSV に変換）
    tags: List[str] = Field(default_factory=list)

class ProjectUpdate(BaseModel):
    # 部分更新用（未指定フィールドは変更しない）
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    repo_url: Optional[str] = None
    app_url: Optional[str] = None
    tech_stack: Optional[str] = None
    story_md: Optional[str] = None
    is_published: Optional[bool] = None
    tags: Optional[List[str]] = None

class ProjectOut(ProjectBase):
    id: int
    created_at: datetime

    # ORM のカラム（models.Project.tags_csv）を取り込むが、レスポンスには出さない
    tags_csv: str = Field(default="", exclude=True)

    # ORM からの取り込みを許可（v2の書き方）
    model_config = ConfigDict(from_attributes=True)

    # レスポンスでは tags[] を自動生成
    @computed_field
    @property
    def tags(self) -> List[str]:
        return [t.strip() for t in (self.tags_csv or "").split(",") if t.strip()]

