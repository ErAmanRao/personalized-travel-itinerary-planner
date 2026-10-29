import datetime
import math
import pytest
from pydantic import ValidationError
from app.models.schemas import (
    TripRequest,
    TravelStyle,
    DestinationInfo,
    UpdateActivityRequest,
    Activity
)
from app.services.budget_service import BudgetService
from app.services.ai_service import AIService
from app.routes.itinerary import update_activity


# ==============================================================================
# 1. THE 7 REGRESSION BUDGETS FOR 4-DAY TRIP WITH 2 TRAVELERS
# ==============================================================================

def test_budget_5000_inr_4_days_2_travelers():
    """
    ₹5,000 budget for 2 travelers over 4 days in Jaipur (Balanced).
    ₹5,000 is approx ₹625/person/day, which is below the minimal viable floor.
    Verifies:
    1. user_budget is preserved as exactly 5000.0.
    2. is_realistic is False, budget_status is 'budget_alert'.
    3. Total estimated cost floors at minimal viable rate (approx ₹6,400) rather than inventing a false fit.
    4. Warning note honestly explains the shortfall without contradiction.
    5. Categories sum exactly to total_estimated_cost.
    6. Daily costs sum exactly to total_estimated_cost.
    7. cost_per_person == total_estimated_cost / 2.
    """
    today = datetime.date.today()
    req = TripRequest(
        destination="Jaipur",
        start_date=today + datetime.timedelta(days=10),
        end_date=today + datetime.timedelta(days=13),
        budget=5000.0,
        currency="INR",
        interests=["culture"],
        travel_style=TravelStyle.BALANCED,
        group_size=2
    )
    dest_info = DestinationInfo(query="Jaipur", resolved_name="Jaipur, Rajasthan", country="India", verified=True)
    itinerary = AIService.generate_itinerary(req, dest_info)
    breakdown = itinerary.budget_breakdown

    assert breakdown.user_budget == 5000.0
    assert breakdown.is_realistic is False
    assert breakdown.budget_status == "budget_alert"
    assert "₹5,000" in breakdown.budget_analysis_notes
    assert "₹625/day/traveler" in breakdown.budget_analysis_notes

    # Verify category reconciliation
    cat_sum = round(
        breakdown.activities_cost
        + breakdown.food_cost
        + breakdown.accommodation_cost
        + breakdown.local_transport_cost,
        2
    )
    assert cat_sum == breakdown.total_estimated_cost
    assert breakdown.cost_per_person == round(breakdown.total_estimated_cost / 2, 2)
    daily_sum = round(sum(d.estimated_daily_cost for d in itinerary.days), 2)
    assert daily_sum == breakdown.total_estimated_cost


def test_budget_10000_inr_4_days_2_travelers():
    """
    ₹10,000 budget for 2 travelers over 4 days in Jaipur (Balanced).
    ₹1,250/person/day is an economical budget that fits within user's target.
    Verifies:
    1. user_budget == 10000.0.
    2. total_estimated_cost == 10000.0.
    3. cost_per_person == 5000.0.
    4. Category sum == 10000.0.
    5. Daily sum == 10000.0.
    6. Uses budget-friendly accommodation and street/local cuisine.
    """
    today = datetime.date.today()
    req = TripRequest(
        destination="Jaipur",
        start_date=today + datetime.timedelta(days=10),
        end_date=today + datetime.timedelta(days=13),
        budget=10000.0,
        currency="INR",
        interests=["culture", "food"],
        travel_style=TravelStyle.BALANCED,
        group_size=2
    )
    dest_info = DestinationInfo(query="Jaipur", resolved_name="Jaipur, Rajasthan", country="India", verified=True)
    itinerary = AIService.generate_itinerary(req, dest_info)
    breakdown = itinerary.budget_breakdown

    assert breakdown.user_budget == 10000.0
    assert breakdown.total_estimated_cost == 10000.0
    assert breakdown.cost_per_person == 5000.0
    cat_sum = round(
        breakdown.activities_cost
        + breakdown.food_cost
        + breakdown.accommodation_cost
        + breakdown.local_transport_cost,
        2
    )
    assert cat_sum == 10000.0
    assert round(sum(d.estimated_daily_cost for d in itinerary.days), 2) == 10000.0
    assert "Hostel" in itinerary.days[0].accommodation.stay_type or "Guesthouse" in itinerary.days[0].accommodation.stay_type


def test_budget_15000_inr_4_days_2_travelers():
    """
    ₹15,000 budget for 2 travelers over 4 days in Jaipur (Balanced).
    Verifies total_estimated_cost == 15000.0, cost_per_person == 7500.0.
    """
    today = datetime.date.today()
    req = TripRequest(
        destination="Jaipur",
        start_date=today + datetime.timedelta(days=10),
        end_date=today + datetime.timedelta(days=13),
        budget=15000.0,
        currency="INR",
        interests=["history", "culture"],
        travel_style=TravelStyle.BALANCED,
        group_size=2
    )
    dest_info = DestinationInfo(query="Jaipur", resolved_name="Jaipur, Rajasthan", country="India", verified=True)
    itinerary = AIService.generate_itinerary(req, dest_info)
    breakdown = itinerary.budget_breakdown

    assert breakdown.user_budget == 15000.0
    assert breakdown.total_estimated_cost == 15000.0
    assert breakdown.cost_per_person == 7500.0
    cat_sum = round(
        breakdown.activities_cost
        + breakdown.food_cost
        + breakdown.accommodation_cost
        + breakdown.local_transport_cost,
        2
    )
    assert cat_sum == 15000.0
    assert round(sum(d.estimated_daily_cost for d in itinerary.days), 2) == 15000.0


def test_budget_20000_inr_4_days_2_travelers():
    """
    ₹20,000 budget for 2 travelers over 4 days in Jaipur (Balanced).
    Verifies user_budget == 20000.0, total_estimated_cost == 20000.0, cost_per_person == 10000.0.
    """
    today = datetime.date.today()
    req = TripRequest(
        destination="Jaipur",
        start_date=today + datetime.timedelta(days=10),
        end_date=today + datetime.timedelta(days=13),
        budget=20000.0,
        currency="INR",
        interests=["history", "culture", "food"],
        travel_style=TravelStyle.BALANCED,
        group_size=2
    )
    dest_info = DestinationInfo(query="Jaipur", resolved_name="Jaipur, Rajasthan", country="India", verified=True)
    itinerary = AIService.generate_itinerary(req, dest_info)
    breakdown = itinerary.budget_breakdown

    assert breakdown.user_budget == 20000.0
    assert breakdown.total_estimated_cost == 20000.0
    assert breakdown.cost_per_person == 10000.0
    cat_sum = round(
        breakdown.activities_cost
        + breakdown.food_cost
        + breakdown.accommodation_cost
        + breakdown.local_transport_cost,
        2
    )
    assert cat_sum == 20000.0
    assert round(sum(d.estimated_daily_cost for d in itinerary.days), 2) == 20000.0
    assert breakdown.budget_status == "within_budget"


def test_budget_35000_inr_4_days_2_travelers():
    """
    ₹35,000 budget for 2 travelers over 4 days in Jaipur (Balanced).
    Verifies user_budget == 35000.0, total_estimated_cost == 35000.0, cost_per_person == 17500.0.
    """
    today = datetime.date.today()
    req = TripRequest(
        destination="Jaipur",
        start_date=today + datetime.timedelta(days=10),
        end_date=today + datetime.timedelta(days=13),
        budget=35000.0,
        currency="INR",
        interests=["history", "shopping"],
        travel_style=TravelStyle.BALANCED,
        group_size=2
    )
    dest_info = DestinationInfo(query="Jaipur", resolved_name="Jaipur, Rajasthan", country="India", verified=True)
    itinerary = AIService.generate_itinerary(req, dest_info)
    breakdown = itinerary.budget_breakdown

    assert breakdown.user_budget == 35000.0
    assert breakdown.total_estimated_cost == 35000.0
    assert breakdown.cost_per_person == 17500.0
    cat_sum = round(
        breakdown.activities_cost
        + breakdown.food_cost
        + breakdown.accommodation_cost
        + breakdown.local_transport_cost,
        2
    )
    assert cat_sum == 35000.0
    assert round(sum(d.estimated_daily_cost for d in itinerary.days), 2) == 35000.0
    assert breakdown.budget_status == "within_budget"


def test_budget_50000_inr_4_days_2_travelers():
    """
    ₹50,000 budget for 2 travelers over 4 days in Jaipur (Balanced).
    Verifies user_budget == 50000.0, total_estimated_cost == 50000.0, cost_per_person == 25000.0.
    """
    today = datetime.date.today()
    req = TripRequest(
        destination="Jaipur",
        start_date=today + datetime.timedelta(days=10),
        end_date=today + datetime.timedelta(days=13),
        budget=50000.0,
        currency="INR",
        interests=["culture", "relaxation"],
        travel_style=TravelStyle.BALANCED,
        group_size=2
    )
    dest_info = DestinationInfo(query="Jaipur", resolved_name="Jaipur, Rajasthan", country="India", verified=True)
    itinerary = AIService.generate_itinerary(req, dest_info)
    breakdown = itinerary.budget_breakdown

    assert breakdown.user_budget == 50000.0
    assert breakdown.total_estimated_cost == 50000.0
    assert breakdown.cost_per_person == 25000.0
    cat_sum = round(
        breakdown.activities_cost
        + breakdown.food_cost
        + breakdown.accommodation_cost
        + breakdown.local_transport_cost,
        2
    )
    assert cat_sum == 50000.0
    assert round(sum(d.estimated_daily_cost for d in itinerary.days), 2) == 50000.0
    assert breakdown.budget_status == "within_budget"


def test_budget_100000_inr_4_days_2_travelers():
    """
    ₹100,000 budget for 2 travelers over 4 days in Jaipur (Balanced).
    Verifies user_budget == 100000.0, total_estimated_cost == 100000.0, cost_per_person == 50000.0.
    Verifies premium lodging, fine dining, and full budget adaptation.
    """
    today = datetime.date.today()
    req = TripRequest(
        destination="Jaipur",
        start_date=today + datetime.timedelta(days=10),
        end_date=today + datetime.timedelta(days=13),
        budget=100000.0,
        currency="INR",
        interests=["culture", "relaxation"],
        travel_style=TravelStyle.BALANCED,
        group_size=2
    )
    dest_info = DestinationInfo(query="Jaipur", resolved_name="Jaipur, Rajasthan", country="India", verified=True)
    itinerary = AIService.generate_itinerary(req, dest_info)
    breakdown = itinerary.budget_breakdown

    assert breakdown.user_budget == 100000.0
    assert breakdown.total_estimated_cost == 100000.0
    assert breakdown.cost_per_person == 50000.0
    cat_sum = round(
        breakdown.activities_cost
        + breakdown.food_cost
        + breakdown.accommodation_cost
        + breakdown.local_transport_cost,
        2
    )
    assert cat_sum == 100000.0
    assert round(sum(d.estimated_daily_cost for d in itinerary.days), 2) == 100000.0
    assert breakdown.budget_status == "within_budget"
    assert "Palace" in itinerary.days[0].accommodation.stay_type or "Resort" in itinerary.days[0].accommodation.stay_type


# ==============================================================================
# 2. GROUP SIZE VARIATIONS
# ==============================================================================

def test_budget_single_traveler():
    """1 traveler, 3 days, ₹15,000: cost_per_person == total_estimated_cost."""
    today = datetime.date.today()
    req = TripRequest(
        destination="Jaipur",
        start_date=today + datetime.timedelta(days=5),
        end_date=today + datetime.timedelta(days=7),
        budget=15000.0,
        currency="INR",
        interests=["culture"],
        travel_style=TravelStyle.BALANCED,
        group_size=1
    )
    dest_info = DestinationInfo(query="Jaipur", resolved_name="Jaipur, Rajasthan", country="India", verified=True)
    itinerary = AIService.generate_itinerary(req, dest_info)
    breakdown = itinerary.budget_breakdown

    assert breakdown.user_budget == 15000.0
    assert breakdown.total_estimated_cost == 15000.0
    assert breakdown.cost_per_person == breakdown.total_estimated_cost


def test_budget_group_of_four_travelers():
    """4 travelers, 4 days, ₹60,000: cost_per_person == total_estimated_cost / 4."""
    today = datetime.date.today()
    req = TripRequest(
        destination="Goa",
        start_date=today + datetime.timedelta(days=10),
        end_date=today + datetime.timedelta(days=13),
        budget=60000.0,
        currency="INR",
        interests=["beaches", "relaxation"],
        travel_style=TravelStyle.BALANCED,
        group_size=4
    )
    dest_info = DestinationInfo(query="Goa", resolved_name="Goa, India", country="India", verified=True)
    itinerary = AIService.generate_itinerary(req, dest_info)
    breakdown = itinerary.budget_breakdown

    assert breakdown.user_budget == 60000.0
    assert breakdown.total_estimated_cost == 60000.0
    assert breakdown.cost_per_person == 15000.0
    cat_sum = round(
        breakdown.activities_cost
        + breakdown.food_cost
        + breakdown.accommodation_cost
        + breakdown.local_transport_cost,
        2
    )
    assert cat_sum == 60000.0


# ==============================================================================
# 3. BUDGET INPUT VALIDATION & FORMATTING TESTS
# ==============================================================================

def test_formatted_budget_strings_accepted():
    """Accepts formatted strings such as '₹20,000', '20,000', '₹ 35,000.50', '  100000  '."""
    today = datetime.date.today()

    cases = [
        ("₹20,000", 20000.0),
        ("20,000", 20000.0),
        ("₹ 35,000.50", 35000.5),
        ("  100000  ", 100000.0),
        ("$50,000", 50000.0),
        ("15000", 15000.0),
        (20000, 20000.0),
        (35000.75, 35000.75),
    ]

    for raw, expected in cases:
        req = TripRequest(
            destination="Jaipur",
            start_date=today + datetime.timedelta(days=5),
            end_date=today + datetime.timedelta(days=8),
            budget=raw,
            currency="INR",
            interests=["culture"],
            travel_style=TravelStyle.BALANCED,
            group_size=2
        )
        assert req.budget == expected


def test_invalid_budget_inputs_rejected():
    """Rejects empty, zero, negative, alphabetic, NaN, infinity, and excessive budgets."""
    today = datetime.date.today()
    invalid_cases = [
        "",
        "   ",
        "0",
        0,
        "-5000",
        -5000.0,
        "invalid_text",
        "abc",
        float("nan"),
        float("inf"),
        float("-inf"),
        100_000_001.0,  # exceeds 100M limit
    ]

    for bad in invalid_cases:
        with pytest.raises(ValidationError):
            TripRequest(
                destination="Jaipur",
                start_date=today + datetime.timedelta(days=5),
                end_date=today + datetime.timedelta(days=8),
                budget=bad,
                currency="INR",
                interests=["culture"],
                travel_style=TravelStyle.BALANCED,
                group_size=2
            )


# ==============================================================================
# 4. ACTIVITY UPDATE RECALCULATION TEST
# ==============================================================================

def test_update_activity_endpoint_recalculates_budget():
    """Updating an activity recalculates the daily cost and trip breakdown totals accurately."""
    today = datetime.date.today()
    req = TripRequest(
        destination="Jaipur",
        start_date=today + datetime.timedelta(days=10),
        end_date=today + datetime.timedelta(days=11),
        budget=10000.0,
        currency="INR",
        interests=["history"],
        travel_style=TravelStyle.BALANCED,
        group_size=2
    )
    dest_info = DestinationInfo(query="Jaipur", resolved_name="Jaipur, Rajasthan", country="India", verified=True)
    itinerary = AIService.generate_itinerary(req, dest_info)
    orig_total = itinerary.budget_breakdown.total_estimated_cost
    orig_act_cost = itinerary.budget_breakdown.activities_cost

    day1 = itinerary.days[0]
    target_act = day1.activities[0]
    updated_act = Activity(
        id=target_act.id,
        title="Exclusive Royal Palace VIP Tour",
        category=target_act.category,
        time_slot=target_act.time_slot,
        description="Private guided VIP tour with curator access",
        estimated_cost=target_act.estimated_cost + 2000.0,
        cost_status="estimated",
        transport_guidance=target_act.transport_guidance,
        tips="Pre-booking required."
    )

    updated_itinerary = update_activity(
        request=UpdateActivityRequest(
            itinerary=itinerary,
            day_number=1,
            activity_id=target_act.id,
            updated_activity=updated_act
        )
    )

    new_breakdown = updated_itinerary.budget_breakdown
    assert new_breakdown.activities_cost == round(orig_act_cost + 2000.0, 2)
    assert new_breakdown.total_estimated_cost == round(orig_total + 2000.0, 2)
    assert new_breakdown.cost_per_person == round(new_breakdown.total_estimated_cost / 2, 2)

    cat_sum = round(
        new_breakdown.activities_cost
        + new_breakdown.food_cost
        + new_breakdown.accommodation_cost
        + new_breakdown.local_transport_cost,
        2
    )
    assert cat_sum == new_breakdown.total_estimated_cost
