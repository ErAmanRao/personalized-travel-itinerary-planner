import pytest
import datetime
from pydantic import ValidationError
from app.models.schemas import TripRequest, TravelStyle


def test_valid_trip_request():
    today = datetime.date.today()
    start = today + datetime.timedelta(days=10)
    end = today + datetime.timedelta(days=14)

    req = TripRequest(
        destination="Jaipur",
        start_date=start,
        end_date=end,
        budget=25000.0,
        currency="INR",
        interests=["history", "culture", "food"],
        travel_style=TravelStyle.BALANCED,
        group_size=2
    )
    assert req.destination == "Jaipur"
    assert req.budget == 25000.0
    assert req.group_size == 2
    assert req.travel_style == TravelStyle.BALANCED


def test_empty_destination_rejected():
    today = datetime.date.today()
    with pytest.raises(ValidationError) as exc:
        TripRequest(
            destination="   ",
            start_date=today + datetime.timedelta(days=5),
            end_date=today + datetime.timedelta(days=8),
            budget=10000.0,
            currency="INR",
            interests=["nature"],
            travel_style=TravelStyle.BUDGET,
            group_size=1
        )
    assert "Destination cannot be empty" in str(exc.value)


def test_end_date_earlier_than_start_date_rejected():
    today = datetime.date.today()
    start = today + datetime.timedelta(days=10)
    end = today + datetime.timedelta(days=5) # 5 days earlier!

    with pytest.raises(ValidationError) as exc:
        TripRequest(
            destination="Goa",
            start_date=start,
            end_date=end,
            budget=20000.0,
            currency="INR",
            interests=["beaches"],
            travel_style=TravelStyle.BALANCED,
            group_size=2
        )
    assert "cannot be earlier than start date" in str(exc.value)


def test_past_travel_date_rejected():
    today = datetime.date.today()
    past_start = today - datetime.timedelta(days=3)
    past_end = today - datetime.timedelta(days=1)

    with pytest.raises(ValidationError) as exc:
        TripRequest(
            destination="Paris",
            start_date=past_start,
            end_date=past_end,
            budget=1500.0,
            currency="EUR",
            interests=["culture"],
            travel_style=TravelStyle.BALANCED,
            group_size=2
        )
    assert "cannot be in the past" in str(exc.value)


def test_zero_or_negative_budget_rejected():
    today = datetime.date.today()
    start = today + datetime.timedelta(days=10)
    end = today + datetime.timedelta(days=14)

    # Zero budget
    with pytest.raises(ValidationError) as exc_zero:
        TripRequest(
            destination="Jaipur",
            start_date=start,
            end_date=end,
            budget=0.0,
            currency="INR",
            interests=["history"],
            travel_style=TravelStyle.BUDGET,
            group_size=1
        )
    assert "greater than 0" in str(exc_zero.value)

    # Negative budget
    with pytest.raises(ValidationError) as exc_neg:
        TripRequest(
            destination="Jaipur",
            start_date=start,
            end_date=end,
            budget=-500.0,
            currency="INR",
            interests=["history"],
            travel_style=TravelStyle.BUDGET,
            group_size=1
        )
    assert "greater than 0" in str(exc_neg.value)


def test_invalid_group_size_rejected():
    today = datetime.date.today()
    start = today + datetime.timedelta(days=5)
    end = today + datetime.timedelta(days=7)

    # 0 travelers
    with pytest.raises(ValidationError) as exc_zero:
        TripRequest(
            destination="Tokyo",
            start_date=start,
            end_date=end,
            budget=50000.0,
            currency="INR",
            interests=["food"],
            travel_style=TravelStyle.BALANCED,
            group_size=0
        )
    assert "at least 1 traveler" in str(exc_zero.value)

    # > 50 travelers
    with pytest.raises(ValidationError) as exc_large:
        TripRequest(
            destination="Tokyo",
            start_date=start,
            end_date=end,
            budget=50000.0,
            currency="INR",
            interests=["food"],
            travel_style=TravelStyle.BALANCED,
            group_size=55
        )
    assert "cannot exceed 50" in str(exc_large.value)


def test_trip_duration_limit():
    today = datetime.date.today()
    start = today + datetime.timedelta(days=5)
    end = today + datetime.timedelta(days=25) # 21 days

    with pytest.raises(ValidationError) as exc:
        TripRequest(
            destination="London",
            start_date=start,
            end_date=end,
            budget=200000.0,
            currency="INR",
            interests=["history"],
            travel_style=TravelStyle.BALANCED,
            group_size=2
        )
    assert "supports itineraries up to 14 days" in str(exc.value)
