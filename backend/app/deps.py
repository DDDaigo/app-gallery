from fastapi import Header, HTTPException, status
from .core.config import settings

def require_admin(x_admin_token: str | None = Header(default=None, alias="X-Admin-Token")):
    if not settings.ADMIN_TOKEN or x_admin_token != settings.ADMIN_TOKEN:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")
    return True
