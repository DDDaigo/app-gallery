from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .db import engine
from .models import Base
from .routers import projects

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 開発用：テーブル自動作成
Base.metadata.create_all(bind=engine)

app.include_router(projects.router, prefix=settings.API_PREFIX)

@app.get("/")
def health():
    return {"ok": True, "name": settings.APP_NAME}
