import datetime
import math
from enum import Enum
from typing import List, Optional, Any
from pydantic import BaseModel, Field, field_validator, model_validator


class TravelStyle(str, Enum):
    BUDGET = "budget"
    BALANCED = "balanced"
    PREMIUM = "premium"


SUPPORTED_CURRENCIES = {
    "INR": {"symbol": "₹", "name": "Indian Rupee", "usd_rate": 0.012},
    "USD": {"symbol": "$", "name": "US Dollar", "usd_rate": 1.0},
    "EUR": {"symbol": "€", "name": "Euro", "usd_rate": 1.08},
    "GBP": {"symbol": "£", "name": "British Pound", "usd_rate": 1.28},
    "JPY": {"symbol": "¥", "name": "Japanese Yen", "usd_rate": 0.0066},
    "AED": {"symbol": "د.إ", "name": "UAE Dirham", "usd_rate": 0.27},
    "AUD": {"symbol": "A$", "name": "Australian Dollar", "usd_rate": 0.65},
    "CAD": {"symbol": "C$", "name": "Canadian Dollar", "usd_rate": 0.73},
    "SGD": {"symbol": "S$", "name": "Singapore Dollar", "usd_rate": 0.75},
}

SUPPORTED_INTERESTS = {
    "nature", "history", "adventure", "culture", "shopping",
    "beaches", "food", "relaxation", "photography", "architecture",
    "nightlife", "wellness"
}


class TripRequest(BaseModel):
    destination: str = Field(..., description="Target destination city, region, or country")
    start_date: datetime.date = Field(..., description="Start date of the trip")
    end_date: datetime.date = Field(..., description="End date of the trip")
    budget: float = Field(..., description="Total trip budget in selected currency")
    currency: str = Field(default="INR", description="Currency code (e.g. INR, USD, EUR)")
    interests: List[str] = Field(..., description="List of user interests")
    travel_style: TravelStyle = Field(default=TravelStyle.BALANCED, description="Travel style")
    group_size: int = Field(default=1, description="Number of travelers in the group")
    special_preferences: Optional[str] = Field(default=None, description="Optional dietary, accessibility, or pace requests")

    @field_validator("destination")
    @classmethod
    def validate_destination(cls, v: str) -> str:
        clean = v.strip()
        if not clean:
            raise ValueError("Destination cannot be empty.")
        if len(clean) < 2:
            raise ValueError("Destination name must be at least 2 characters long.")
        if len(clean) > 80:
            raise ValueError("Destination name is too long (maximum 80 characters).")
        return clean

    @field_validator("budget", mode="before")
    @classmethod
    def validate_budget(cls, v: Any) -> float:
        if v is None:
            raise ValueError("Trip budget cannot be empty.")
        if isinstance(v, str):
            clean = v.strip()
            if not clean:
                raise ValueError("Trip budget cannot be empty.")
            for sym in [
                "₹", "$", "€", "£", "¥", "A$", "C$", "S$",
                "INR", "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "SGD",
                "Rs.", "Rs", "rs.", "rs", "?"
            ]:
                clean = clean.replace(sym, "")
            clean = clean.replace(",", "").strip()
            try:
                num = float(clean)
            except (ValueError, TypeError):
                raise ValueError(f"Trip budget must be a valid positive number. Received: '{v}'")
        elif isinstance(v, (int, float)):
            num = float(v)
        else:
            raise ValueError("Trip budget must be a valid numeric amount.")

        if math.isnan(num) or math.isinf(num):
            raise ValueError("Trip budget cannot be NaN or infinite.")
        if num <= 0:
            raise ValueError("Trip budget must be a positive number greater than 0.")
        if num > 100_000_000.0:
            raise ValueError("Trip budget exceeds the maximum supported limit (100,000,000).")

        return round(num, 2)

    @field_validator("group_size")
    @classmethod
    def validate_group_size(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Group size must be at least 1 traveler.")
        if v > 50:
            raise ValueError("Group size cannot exceed 50 travelers.")
        return v

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        code = v.strip().upper()
        if code not in SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency '{v}'. Supported: {', '.join(SUPPORTED_CURRENCIES.keys())}")
        return code

    @field_validator("interests")
    @classmethod
    def validate_interests(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("Please select at least one interest.")
        cleaned = [i.strip().lower() for i in v if i.strip()]
        if not cleaned:
            raise ValueError("Please select at least one valid interest.")
        return cleaned

    @model_validator(mode="after")
    def validate_dates(self) -> "TripRequest":
        today = datetime.date.today()
        if self.start_date < today:
            raise ValueError(f"Travel start date ({self.start_date}) cannot be in the past. Today is {today}.")
        if self.end_date < self.start_date:
            raise ValueError(f"End date ({self.end_date}) cannot be earlier than start date ({self.start_date}).")
        
        trip_duration = (self.end_date - self.start_date).days + 1
        if trip_duration > 14:
            raise ValueError(f"Requested trip duration is {trip_duration} days. WanderWise currently supports itineraries up to 14 days.")
        return self


class DestinationInfo(BaseModel):
    query: str
    resolved_name: str
    country: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    verified: bool = True
    verification_source: str = "curated_database"
    image_url: Optional[str] = None
    image_source: Optional[str] = None
    photographer_name: Optional[str] = None
    photographer_url: Optional[str] = None
    image_attribution: Optional[str] = None
    image_status: str = Field(default="verified", description="verified, api_result, or unavailable")


class Activity(BaseModel):
    id: str = Field(..., description="Unique activity ID")
    title: str = Field(..., description="Title of the attraction or activity")
    time_slot: str = Field(..., description="Time of day or time range (e.g. 09:30 - 12:00)")
    category: str = Field(..., description="Category: Attraction, Culture, Nature, Food, Shopping, etc.")
    description: str = Field(..., description="Insightful description and visitor tips")
    estimated_cost: float = Field(default=0.0, ge=0.0, description="Estimated activity cost per group")
    cost_status: str = Field(default="estimated", description="Label: estimated or free")
    transport_guidance: Optional[str] = Field(default=None, description="Guidance to get to/from this activity")
    tips: Optional[str] = Field(default=None, description="Practical travel tip for this spot")


class MealOption(BaseModel):
    meal_type: str = Field(..., description="Breakfast, Lunch, or Dinner")
    suggestion: str = Field(..., description="Name of restaurant, dish, or market")
    cuisine_type: str = Field(..., description="Type of cuisine or dining style")
    estimated_cost: float = Field(default=0.0, ge=0.0, description="Estimated meal cost for group")


class AccommodationGuidance(BaseModel):
    recommended_area: str = Field(..., description="Neighborhood or district best for staying")
    stay_type: str = Field(..., description="e.g. 3-Star Boutique Hotel, Eco-Resort, Guesthouse")
    estimated_nightly_cost: float = Field(default=0.0, ge=0.0, description="Estimated cost per night")
    tips: str = Field(..., description="Booking advice or accessibility considerations")


class DayPlan(BaseModel):
    day_number: int = Field(..., ge=1)
    date: str = Field(..., description="Date string YYYY-MM-DD")
    theme: str = Field(..., description="Day focus or theme")
    activities: List[Activity]
    meals: List[MealOption]
    accommodation: AccommodationGuidance
    daily_transport_summary: str
    daily_transport_cost: float = Field(default=0.0, ge=0.0, description="Estimated local transit cost for group for this day")
    estimated_daily_cost: float
    sensible_schedule_note: str = Field(
        ...,
        description="Explanation of why this day's sequence is sensible and avoids long transit"
    )


class BudgetBreakdown(BaseModel):
    currency: str
    currency_symbol: str
    activities_cost: float
    food_cost: float
    accommodation_cost: float
    local_transport_cost: float
    total_estimated_cost: float
    cost_per_person: float
    user_budget: float
    cost_type: str = "estimated"
    budget_status: str = Field(
        ...,
        description="'within_budget', 'exceeds_budget', or 'budget_alert'"
    )
    is_realistic: bool = True
    recommended_minimum_budget: Optional[float] = None
    budget_analysis_notes: str


class Itinerary(BaseModel):
    id: str
    title: str
    destination: DestinationInfo
    start_date: str
    end_date: str
    total_days: int
    travel_style: TravelStyle
    group_size: int
    currency: str
    days: List[DayPlan]
    budget_breakdown: BudgetBreakdown
    why_it_matches: str
    generation_source: str = Field(
        default="fallback_curated_engine",
        description="Indicates whether generated by 'ai_model' or 'fallback_curated_engine'"
    )
    model_name: Optional[str] = None
    disclaimer: str = Field(
        default="All costs, schedules, and recommendations are estimated planning guidance and require independent verification before travel.",
        description="Honest travel disclaimer"
    )
    created_at: str


class RegenerateDayRequest(BaseModel):
    itinerary: Itinerary
    day_number: int = Field(..., ge=1)
    focus_note: Optional[str] = Field(default=None, description="Optional custom focus for the regenerated day")


class RefineTripRequest(BaseModel):
    itinerary: Itinerary
    refinement_instruction: str = Field(..., min_length=3, description="What to modify across the trip")


class UpdateActivityRequest(BaseModel):
    itinerary: Itinerary
    day_number: int = Field(..., ge=1)
    activity_id: str
    updated_activity: Activity


class TripSummary(BaseModel):
    id: str
    title: str
    destination_name: str
    country: str
    start_date: str
    end_date: str
    total_days: int
    travel_style: str
    group_size: int
    currency: str
    total_estimated_cost: float
    created_at: str
    image_url: Optional[str] = None


class SaveTripRequest(BaseModel):
    itinerary: Itinerary
    user_id: Optional[str] = None
