import logging
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import (
    TripRequest,
    Itinerary,
    RegenerateDayRequest,
    RefineTripRequest,
    UpdateActivityRequest
)
from app.services.destination_service import DestinationService
from app.services.ai_service import AIService
from app.services.budget_service import BudgetService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/itinerary", tags=["Itinerary"])


@router.post("/generate", response_model=Itinerary, status_code=status.HTTP_200_OK)
def generate_itinerary(request: TripRequest):
    """
    Validates input parameters and destination, then generates a complete
    day-by-day travel itinerary with budget breakdown and schedule guidance.
    """
    try:
        # Step 1: Destination verification
        dest_info = DestinationService.verify_destination(request.destination)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Destination validation error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Destination verification unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to verify destination at this time. Please try again."
        )

    # Step 2: Generate itinerary
    try:
        itinerary = AIService.generate_itinerary(request, dest_info)
        return itinerary
    except Exception as e:
        logger.error(f"Failed to generate itinerary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Itinerary generation failed: {str(e)}"
        )


@router.post("/regenerate-day", response_model=Itinerary)
def regenerate_day(request: RegenerateDayRequest):
    """
    Regenerates a single day in the itinerary while preserving all other days.
    """
    try:
        updated = AIService.regenerate_single_day(request)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to regenerate day: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to regenerate requested day. Please retry."
        )


@router.post("/refine", response_model=Itinerary)
def refine_itinerary(request: RefineTripRequest):
    """
    Applies user refinement instructions across the full itinerary.
    """
    try:
        refined = AIService.refine_itinerary(request)
        return refined
    except Exception as e:
        logger.error(f"Failed to refine itinerary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refine itinerary. Please retry."
        )


@router.post("/update-activity", response_model=Itinerary)
def update_activity(request: UpdateActivityRequest):
    """
    Updates an activity inside a specific day and recalculates day and trip budget totals.
    """
    itinerary = request.itinerary
    day_number = request.day_number
    activity_id = request.activity_id
    updated_activity = request.updated_activity

    found = False
    for day in itinerary.days:
        if day.day_number == day_number:
            for idx, act in enumerate(day.activities):
                if act.id == activity_id:
                    day.activities[idx] = updated_activity
                    found = True
                    break
            if found:
                # Recalculate day.estimated_daily_cost
                act_cost = sum(a.estimated_cost for a in day.activities)
                meal_cost = sum(m.estimated_cost for m in day.meals)
                stay_cost = day.accommodation.estimated_nightly_cost
                trans_cost = getattr(day, "daily_transport_cost", 0.0)
                day.estimated_daily_cost = round(act_cost + meal_cost + stay_cost + trans_cost, 2)
                break

    if not found:
        raise HTTPException(status_code=404, detail="Activity or day not found in itinerary.")

    is_domestic = (
        itinerary.destination.country.lower() == "india"
        if itinerary.destination and itinerary.destination.country
        else False
    )
    # Rebuild budget breakdown with exact day items
    itinerary.budget_breakdown = BudgetService.build_breakdown_from_days(
        days=itinerary.days,
        user_budget=itinerary.budget_breakdown.user_budget,
        currency=itinerary.budget_breakdown.currency,
        total_days=itinerary.total_days,
        group_size=itinerary.group_size,
        travel_style=itinerary.travel_style,
        is_domestic=is_domestic
    )

    return itinerary
