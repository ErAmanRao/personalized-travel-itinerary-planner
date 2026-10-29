from fastapi import APIRouter
from app.config import settings
from app.services.supabase_service import SupabaseService

router = APIRouter(tags=["Health & Status"])


@router.get("/health")
def health_check():
    """
    Returns API health status, configured AI engines, and Supabase integration status.
    """
    ai_provider = "none"
    if settings.GEMINI_API_KEY:
        ai_provider = f"Google Gemini ({settings.GEMINI_MODEL})"
    elif settings.OPENAI_API_KEY:
        ai_provider = f"OpenAI ({settings.OPENAI_MODEL})"

    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "ai_engine": {
            "configured": settings.has_ai_configured,
            "provider": ai_provider,
            "fallback_engine": "WanderWise Curated Rules Engine (Active)"
        },
        "database": SupabaseService.get_status()
    }
