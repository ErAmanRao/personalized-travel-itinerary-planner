import logging
from typing import List, Optional, Dict, Any
import httpx
from app.config import settings
from app.models.schemas import Itinerary, TripSummary

logger = logging.getLogger(__name__)

# In-memory storage for preview mode when Supabase is not configured
IN_MEMORY_PREVIEW_TRIPS: Dict[str, Dict[str, Any]] = {}


class SupabaseService:
    @classmethod
    def is_configured(cls) -> bool:
        return settings.has_supabase_configured

    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        return {
            "configured": cls.is_configured(),
            "url_set": bool(settings.SUPABASE_URL),
            "anon_key_set": bool(settings.SUPABASE_ANON_KEY),
            "service_role_set": bool(settings.SUPABASE_SERVICE_ROLE_KEY),
            "mode": "supabase_database" if cls.is_configured() else "preview_in_memory",
            "message": (
                "Supabase is connected and ready for persistent trip storage."
                if cls.is_configured()
                else "Supabase is not configured. WanderWise is operating in in-memory preview mode. Trips are saved for the current session only."
            )
        }

    @classmethod
    def save_trip(cls, itinerary: Itinerary, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Saves trip to Supabase if configured; otherwise stores in memory preview.
        """
        trip_record = {
            "id": itinerary.id,
            "user_id": user_id or "anonymous-preview-user",
            "title": itinerary.title,
            "destination_name": itinerary.destination.resolved_name,
            "country": itinerary.destination.country,
            "start_date": itinerary.start_date,
            "end_date": itinerary.end_date,
            "total_days": itinerary.total_days,
            "travel_style": itinerary.travel_style.value,
            "group_size": itinerary.group_size,
            "currency": itinerary.currency,
            "total_estimated_cost": itinerary.budget_breakdown.total_estimated_cost,
            "image_url": itinerary.destination.image_url,
            "itinerary_data": itinerary.model_dump(),
            "created_at": itinerary.created_at
        }

        if cls.is_configured():
            try:
                headers = {
                    "apikey": settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY,
                    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                }
                with httpx.Client(timeout=10.0) as client:
                    resp = client.post(
                        f"{settings.SUPABASE_URL.rstrip('/')}/rest/v1/trips",
                        json=trip_record,
                        headers=headers
                    )
                    if resp.status_code in (200, 201):
                        return {
                            "success": True,
                            "persisted_to_db": True,
                            "storage_mode": "supabase_database",
                            "trip_id": itinerary.id,
                            "message": "Trip successfully saved to Supabase database."
                        }
                    else:
                        logger.error(f"Supabase save error {resp.status_code}: {resp.text}")
            except Exception as e:
                logger.error(f"Failed to save trip to Supabase: {e}")

        # In-memory storage preview
        IN_MEMORY_PREVIEW_TRIPS[itinerary.id] = trip_record
        return {
            "success": True,
            "persisted_to_db": False,
            "storage_mode": "preview_in_memory",
            "trip_id": itinerary.id,
            "message": "Trip saved to in-memory preview mode (Supabase not configured or unreachable)."
        }

    @classmethod
    def get_user_trips(cls, user_id: Optional[str] = None) -> List[TripSummary]:
        """
        Retrieves all trips for a user.
        """
        summaries: List[TripSummary] = []

        if cls.is_configured():
            try:
                headers = {
                    "apikey": settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY,
                    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY}",
                }
                url = f"{settings.SUPABASE_URL.rstrip('/')}/rest/v1/trips?select=*&order=created_at.desc"
                if user_id:
                    url += f"&user_id=eq.{user_id}"

                with httpx.Client(timeout=10.0) as client:
                    resp = client.get(url, headers=headers)
                    if resp.status_code == 200:
                        rows = resp.json()
                        for r in rows:
                            summaries.append(TripSummary(
                                id=r["id"],
                                title=r["title"],
                                destination_name=r["destination_name"],
                                country=r.get("country", ""),
                                start_date=r["start_date"],
                                end_date=r["end_date"],
                                total_days=r["total_days"],
                                travel_style=r["travel_style"],
                                group_size=r["group_size"],
                                currency=r["currency"],
                                total_estimated_cost=float(r["total_estimated_cost"]),
                                created_at=r["created_at"],
                                image_url=r.get("image_url")
                            ))
                        return summaries
            except Exception as e:
                logger.error(f"Failed to fetch trips from Supabase: {e}")

        # From in-memory preview
        for r in IN_MEMORY_PREVIEW_TRIPS.values():
            if not user_id or r.get("user_id") == user_id or r.get("user_id") == "anonymous-preview-user":
                summaries.append(TripSummary(
                    id=r["id"],
                    title=r["title"],
                    destination_name=r["destination_name"],
                    country=r.get("country", ""),
                    start_date=r["start_date"],
                    end_date=r["end_date"],
                    total_days=r["total_days"],
                    travel_style=r["travel_style"],
                    group_size=r["group_size"],
                    currency=r["currency"],
                    total_estimated_cost=float(r["total_estimated_cost"]),
                    created_at=r["created_at"],
                    image_url=r.get("image_url")
                ))

        summaries.sort(key=lambda s: s.created_at, reverse=True)
        return summaries

    @classmethod
    def get_trip_by_id(cls, trip_id: str) -> Optional[Itinerary]:
        """
        Retrieves full itinerary details.
        """
        if cls.is_configured():
            try:
                headers = {
                    "apikey": settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY,
                    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY}",
                }
                url = f"{settings.SUPABASE_URL.rstrip('/')}/rest/v1/trips?id=eq.{trip_id}&select=*"
                with httpx.Client(timeout=10.0) as client:
                    resp = client.get(url, headers=headers)
                    if resp.status_code == 200:
                        rows = resp.json()
                        if rows:
                            return Itinerary.model_validate(rows[0]["itinerary_data"])
            except Exception as e:
                logger.error(f"Failed to get trip from Supabase: {e}")

        # From in-memory
        if trip_id in IN_MEMORY_PREVIEW_TRIPS:
            return Itinerary.model_validate(IN_MEMORY_PREVIEW_TRIPS[trip_id]["itinerary_data"])
        return None

    @classmethod
    def delete_trip(cls, trip_id: str) -> bool:
        if cls.is_configured():
            try:
                headers = {
                    "apikey": settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY,
                    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY}",
                }
                url = f"{settings.SUPABASE_URL.rstrip('/')}/rest/v1/trips?id=eq.{trip_id}"
                with httpx.Client(timeout=10.0) as client:
                    resp = client.delete(url, headers=headers)
                    if resp.status_code in (200, 204):
                        return True
            except Exception as e:
                logger.error(f"Failed to delete trip from Supabase: {e}")

        if trip_id in IN_MEMORY_PREVIEW_TRIPS:
            del IN_MEMORY_PREVIEW_TRIPS[trip_id]
            return True
        return False
