from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Boolean, DateTime
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(120), index=True)
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String(512), default="")
    repo_url: Mapped[str] = mapped_column(String(512), default="")
    app_url: Mapped[str] = mapped_column(String(512), default="")
    tech_stack: Mapped[str] = mapped_column(String(256), default="Vue3, Tailwind, FastAPI")
    story_md: Mapped[str] = mapped_column(Text, default="")   # 制作談（Markdown）
    tags_csv: Mapped[str] = mapped_column(Text, default="")   # まずはCSVで簡易に運用
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
