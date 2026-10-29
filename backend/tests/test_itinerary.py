import pytest
import datetime
from app.models.schemas import (
    TripRequest,
    TravelStyle,
    DestinationInfo,
    RegenerateDayRequest,
    RefineTripRequest
)
from app.services.ai_service import AIService


def test_itinerary_generation_without_ai_keys():
    today = datetime.date.today()
    req = TripRequest(
        destination="Jaipur",
        start_date=today + datetime.timedelta(days=10),
        end_date=today + datetime.timedelta(days=12), # 3 days
        budget=30000.0,
        currency="INR",
        interests=["culture", "history"],
        travel_style=TravelStyle.BALANCED,
        group_size=2
    )
    dest_info = DestinationInfo(
        query="Jaipur",
        resolved_name="Jaipur, Rajasthan",
        country="India",
        verified=True,
        verification_source="curated_travel_registry",
        image_url="https://images.unsplash.com/photo-1599661046289-e31897846e41"
    )

    itinerary = AIService.generate_itinerary(req, dest_info)
    assert itinerary is not None
    assert itinerary.total_days == 3
    assert len(itinerary.days) == 3
    assert itinerary.generation_source == "fallback_curated_engine"
    assert "Jaipur" in itinerary.title

    for day in itinerary.days:
        assert day.day_number in [1, 2, 3]
        assert len(day.activities) >= 2
        for act in day.activities:
            assert act.title != ""
            assert act.estimated_cost >= 0.0
            assert act.transport_guidance is not None
        assert len(day.meals) == 3
        assert day.accommodation is not None
        assert day.estimated_daily_cost > 0


def test_regenerate_single_day():
    today = datetime.date.today()
    req = TripRequest(
        destination="Paris",
        start_date=today + datetime.timedelta(days=10),
        end_date=today + datetime.timedelta(days=12),
        budget=120000.0,
        currency="INR",
        interests=["culture"],
        travel_style=TravelStyle.BALANCED,
        group_size=2
    )
    dest_info = DestinationInfo(
        query="Paris",
        resolved_name="Paris, France",
        country="France",
        verified=True,
        verification_source="curated_travel_registry"
    )

    itinerary = AIService.generate_itinerary(req, dest_info)
    orig_day1_theme = itinerary.days[0].theme

    # Regenerate Day 2 with custom focus
    regen_req = RegenerateDayRequest(
        itinerary=itinerary,
        day_number=2,
        focus_note="Art Galleries and River Cafes"
    )
    updated_itinerary = AIService.regenerate_single_day(regen_req)

    # Day 1 must remain untouched
    assert updated_itinerary.days[0].theme == orig_day1_theme
    # Day 2 must reflect regeneration
    assert "Art Galleries and River Cafes" in updated_itinerary.days[1].theme


def test_refine_itinerary():
    today = datetime.date.today()
    req = TripRequest(
        destination="Tokyo",
        start_date=today + datetime.timedelta(days=15),
        end_date=today + datetime.timedelta(days=17),
        budget=150000.0,
        currency="INR",
        interests=["food"],
        travel_style=TravelStyle.BALANCED,
        group_size=2
    )
    dest_info = DestinationInfo(
        query="Tokyo",
        resolved_name="Tokyo, Japan",
        country="Japan",
        verified=True,
        verification_source="curated_travel_registry"
    )

    itinerary = AIService.generate_itinerary(req, dest_info)
    refine_req = RefineTripRequest(
        itinerary=itinerary,
        refinement_instruction="All vegetarian meals and relaxed pace"
    )
    refined = AIService.refine_itinerary(refine_req)

    for day in refined.days:
        for meal in day.meals:
            assert "Vegetarian" in meal.suggestion or "Veg" in meal.cuisine_type
