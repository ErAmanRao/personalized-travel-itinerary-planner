import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # Supabase credentials (optional, fallback provided if missing)
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    
    # Destination Photo API (Optional: if blank, uses verified editorial registry & open travel knowledge)
    UNSPLASH_ACCESS_KEY: str = ""
    
    # App Settings
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"
    ENVIRONMENT: str = "development"
    APP_NAME: str = "WanderWise API"
    APP_VERSION: str = "1.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def has_ai_configured(self) -> bool:
        return bool(self.GEMINI_API_KEY.strip() or self.OPENAI_API_KEY.strip())

    @property
    def has_supabase_configured(self) -> bool:
        return bool(self.SUPABASE_URL.strip() and (self.SUPABASE_ANON_KEY.strip() or self.SUPABASE_SERVICE_ROLE_KEY.strip()))


settings = Settings()
