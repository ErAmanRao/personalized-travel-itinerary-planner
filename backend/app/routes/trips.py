from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from app.models.schemas import SaveTripRequest, TripSummary, Itinerary
from app.services.supabase_service import SupabaseService

router = APIRouter(prefix="/trips", tags=["Saved Trips"])


@router.get("/status")
def get_storage_status():
    """
    Returns current database connection and storage status (Supabase vs In-Memory Preview).
    """
    return SupabaseService.get_status()


@router.post("", status_code=status.HTTP_201_CREATED)
def save_trip(request: SaveTripRequest):
    """
    Saves an itinerary to Supabase (or in-memory preview if Supabase is unconfigured).
    """
    result = SupabaseService.save_trip(request.itinerary, request.user_id)
    return result


@router.get("", response_model=List[TripSummary])
def list_trips(user_id: Optional[str] = Query(default=None, description="Optional user ID filter")):
    """
    Lists saved trip summaries for the authenticated or preview user.
    """
    trips = SupabaseService.get_user_trips(user_id)
    return trips


@router.get("/{trip_id}", response_model=Itinerary)
def get_trip(trip_id: str):
    """
    Retrieves full itinerary by trip ID.
    """
    trip = SupabaseService.get_trip_by_id(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found.")
    return trip


@router.delete("/{trip_id}")
def delete_trip(trip_id: str):
    """
    Deletes a saved trip by ID.
    """
    success = SupabaseService.delete_trip(trip_id)
    if not success:
        raise HTTPException(status_code=404, detail="Trip not found or could not be deleted.")
    return {"success": True, "message": "Trip successfully deleted."}
