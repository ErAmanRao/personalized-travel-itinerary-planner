import pytest
import datetime
from fastapi import HTTPException
from app.routes import health, destinations, itinerary, trips
from app.models.schemas import TripRequest, TravelStyle, SaveTripRequest


def test_health_check_endpoint():
    data = health.health_check()
    assert data["status"] == "healthy"
    assert "ai_engine" in data
    assert "database" in data
    assert data["database"]["mode"] in ["supabase_database", "preview_in_memory"]


def test_destination_verify_endpoint_valid():
    data = destinations.verify_destination(query="Jaipur")
    assert data.verified is True
    assert "Jaipur" in data.resolved_name


def test_destination_verify_endpoint_invalid():
    with pytest.raises(HTTPException) as exc:
        destinations.verify_destination(query="asdfghjk")
    assert exc.value.status_code == 400
    assert "could not be verified" in exc.value.detail


def test_itinerary_generate_endpoint_success():
    today = datetime.date.today()
    req = TripRequest(
        destination="Goa",
        start_date=today + datetime.timedelta(days=10),
        end_date=today + datetime.timedelta(days=13),
        budget=35000.0,
        currency="INR",
        interests=["beaches", "relaxation", "food"],
        travel_style=TravelStyle.BALANCED,
        group_size=2
    )
    result = itinerary.generate_itinerary(req)
    assert "Goa" in result.title
    assert len(result.days) == 4
    assert result.budget_breakdown.total_estimated_cost > 0


def test_trips_save_and_list_preview():
    today = datetime.date.today()
    req = TripRequest(
        destination="Udaipur",
        start_date=today + datetime.timedelta(days=15),
        end_date=today + datetime.timedelta(days=17),
        budget=40000.0,
        currency="INR",
        interests=["culture", "photography"],
        travel_style=TravelStyle.BALANCED,
        group_size=2
    )
    itin = itinerary.generate_itinerary(req)

    # Save trip
    save_result = trips.save_trip(SaveTripRequest(itinerary=itin))
    assert save_result["success"] is True
    assert save_result["trip_id"] == itin.id

    # List trips
    user_trips = trips.list_trips()
    assert any(t.id == itin.id for t in user_trips)

    # Get specific trip
    retrieved = trips.get_trip(trip_id=itin.id)
    assert retrieved.id == itin.id
