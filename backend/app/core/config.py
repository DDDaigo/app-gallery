from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "App Gallery"
    API_PREFIX: str = "/api"
    DB_URL: str  # compose の env から渡す
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://gallery.localhost"]
    ADMIN_TOKEN: str = ""  # ← 追加（backend/.env で設定）

settings = Settings()
