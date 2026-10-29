from fastapi import APIRouter, HTTPException, Query
from app.services.destination_service import DestinationService
from app.models.schemas import DestinationInfo

router = APIRouter(prefix="/destinations", tags=["Destinations"])


@router.get("/verify", response_model=DestinationInfo)
def verify_destination(
    query: str = Query(..., min_length=1, description="Destination query to verify")
):
    """
    Verifies that a destination exists, resolves its geographic jurisdiction,
    and returns verified status or raises 400 Bad Request if unverified/gibberish.
    """
    try:
        dest_info = DestinationService.verify_destination(query)
        return dest_info
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
