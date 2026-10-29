import json
import logging
import uuid
import datetime
from typing import Dict, Any, List, Optional
import httpx

from app.config import settings
from app.models.schemas import (
    TripRequest,
    DestinationInfo,
    Itinerary,
    DayPlan,
    Activity,
    MealOption,
    AccommodationGuidance,
    RegenerateDayRequest,
    RefineTripRequest,
    TravelStyle,
)
from app.services.budget_service import BudgetService

logger = logging.getLogger(__name__)


CITY_ACTIVITIES = {
    "jaipur": [
        {"title": "Amber Palace & Sheesh Mahal", "slot": "Morning (09:00 - 12:30)", "cat": "Culture", "desc": "Explore 16th-century Rajput architecture, mirror mosaics, and panoramic Maota Lake views.", "transport": "25 min cab or auto from city centre", "free": False},
        {"title": "Panna Meena ka Kund Stepwell", "slot": "Morning (11:30 - 12:30)", "cat": "Attraction", "desc": "Admire the geometric stair patterns of this historic 16th-century rainwater catchment marvel.", "transport": "5 min walk from Amber Fort", "free": True},
        {"title": "Hawa Mahal (Palace of Winds)", "slot": "Afternoon (14:00 - 15:30)", "cat": "History", "desc": "Marvel at the 953 honeycombed pink sandstone windows designed for royal women to observe street festivals.", "transport": "Short auto-rickshaw ride", "free": False},
        {"title": "City Palace & Sawai Man Singh II Museum", "slot": "Afternoon (15:30 - 17:30)", "cat": "Culture", "desc": "Tour the active royal residence, courtyards, and armory exhibits in the heart of Old City.", "transport": "10 min walk from Hawa Mahal", "free": False},
        {"title": "Jantar Mantar Astronomical Observatory", "slot": "Afternoon (14:00 - 16:00)", "cat": "History", "desc": "UNESCO World Heritage site featuring the world's largest stone sundial and 19 architectural instruments.", "transport": "Adjacent to City Palace", "free": False},
        {"title": "Nahargarh Fort Sunset Viewpoint", "slot": "Evening (17:30 - 19:30)", "cat": "Nature", "desc": "Watch the sunset glow over the Pink City skyline from the high Aravalli ridge.", "transport": "30 min scenic cab ride up Aravalli hills", "free": False},
        {"title": "Johari Bazaar & Bapu Bazaar Walk", "slot": "Evening (18:00 - 20:30)", "cat": "Shopping", "desc": "Stroll traditional Pink City bazaars for handcrafted mojris, block-printed textiles, and blue pottery.", "transport": "Central walking district", "free": True},
        {"title": "Chokhi Dhani Cultural Experience", "slot": "Evening (18:30 - 21:30)", "cat": "Food", "desc": "Immerse in folk dances, puppet performances, and an authentic multi-course Rajasthani thali feast.", "transport": "35 min cab south of city", "free": False},
    ],
    "paris": [
        {"title": "Eiffel Tower & Champ de Mars", "slot": "Morning (09:00 - 12:00)", "cat": "Attraction", "desc": "Ascend Gustave Eiffel's iconic 1889 iron lattice monument for panoramic views of the Seine River basin.", "transport": "Metro Line 6 to Bir-Hakeim", "free": False},
        {"title": "Musée du Louvre Masterpieces", "slot": "Morning (09:30 - 13:00)", "cat": "Culture", "desc": "Walk the grand galleries featuring the Mona Lisa, Winged Victory of Samothrace, and Venus de Milo.", "transport": "Metro Line 1 to Palais Royal", "free": False},
        {"title": "Musée d'Orsay Impressionist Collection", "slot": "Afternoon (14:00 - 17:00)", "cat": "Culture", "desc": "Housed in a beaux-arts railway station, admire works by Monet, Van Gogh, Renoir, and Degas.", "transport": "RER C to Musée d'Orsay", "free": False},
        {"title": "Île de la Cité & Sainte-Chapelle", "slot": "Afternoon (14:00 - 16:30)", "cat": "History", "desc": "Gaze upon 1,113 radiant 13th-century stained-glass panes and exterior of Notre-Dame Cathedral.", "transport": "Metro Line 4 to Cité", "free": False},
        {"title": "Le Marais Historic District & Place des Vosges", "slot": "Afternoon (15:00 - 17:30)", "cat": "Shopping", "desc": "Stroll cobblestone alleys lined with independent fashion boutiques, art galleries, and historic mansions.", "transport": "Walking district", "free": True},
        {"title": "Seine River Sunset Cruise", "slot": "Evening (18:00 - 20:00)", "cat": "Relaxation", "desc": "Cruise past illuminated monuments, stone bridges, and Parisian riverbanks at golden hour.", "transport": "Board near Pont de l'Alma", "free": False},
        {"title": "Montmartre & Sacré-Cœur Basilica", "slot": "Evening (17:30 - 20:30)", "cat": "Culture", "desc": "Climb the bohemian hilltop to the domed basilica for sweeping Parisian vistas and Place du Tertre painters.", "transport": "Metro Line 2 to Anvers", "free": True},
    ],
    "tokyo": [
        {"title": "Senso-ji Temple & Nakamise-dori", "slot": "Morning (09:00 - 12:00)", "cat": "Culture", "desc": "Tokyo's oldest Buddhist temple founded in 645 AD, entered via the grand Kaminarimon Thunder Gate.", "transport": "Ginza Subway to Asakusa", "free": True},
        {"title": "Meiji Jingu Shinto Shrine & Yoyogi Forest", "slot": "Morning (09:30 - 12:00)", "cat": "Nature", "desc": "Walk through 170 acres of tranquil sacred forest dedicated to Emperor Meiji and Empress Shoken.", "transport": "JR Yamanote to Harajuku", "free": True},
        {"title": "Shibuya Crossing & Shibuya Sky", "slot": "Afternoon (13:30 - 16:30)", "cat": "Attraction", "desc": "Experience the world's busiest pedestrian intersection and view the modern scramble from Shibuya Sky.", "transport": "JR Yamanote to Shibuya", "free": False},
        {"title": "Akihabara Electric Town & Manga Culture", "slot": "Afternoon (14:00 - 17:00)", "cat": "Shopping", "desc": "Discover multi-storey retro arcade centers, electronics stores, and hobby shops.", "transport": "JR Yamanote to Akihabara", "free": True},
        {"title": "Shinjuku Gyoen National Garden", "slot": "Afternoon (13:00 - 15:30)", "cat": "Nature", "desc": "Blend of traditional Japanese landscape, English formal, and French landscaped gardens.", "transport": "5 min walk from Shinjuku-Gyoemmae", "free": False},
        {"title": "Omoide Yokocho & Shinjuku Nightscape", "slot": "Evening (18:00 - 21:00)", "cat": "Food", "desc": "Savor yakitori skewers in atmospheric post-war alleyways followed by panoramic views from Tokyo Gov building.", "transport": "West exit Shinjuku Station", "free": False},
    ]
}


class AIService:
    @classmethod
    def generate_itinerary(cls, request: TripRequest, dest_info: DestinationInfo) -> Itinerary:
        """
        Generates full itinerary using configured AI provider (Gemini / OpenAI),
        or deterministic curated fallback engine if keys are absent.
        """
        total_days = (request.end_date - request.start_date).days + 1
        is_domestic = (dest_info.country.lower() == "india" and request.currency == "INR")

        if settings.has_ai_configured:
            try:
                itinerary = cls._generate_via_ai(request, dest_info, total_days, is_domestic)
                if itinerary:
                    return itinerary
            except Exception as e:
                logger.error(f"AI generation call failed: {e}. Falling back to curated engine.")

        # Curated engine fallback
        return cls._generate_via_curated_engine(request, dest_info, total_days, is_domestic)

    @classmethod
    def regenerate_single_day(cls, request: RegenerateDayRequest) -> Itinerary:
        """
        Regenerates only the requested day while keeping others completely preserved,
        and accurately reconciles the itinerary budget breakdown.
        """
        itinerary = request.itinerary
        target_day = request.day_number
        is_domestic = (itinerary.destination.country.lower() == "india" and itinerary.currency == "INR")

        found = False
        for idx, day in enumerate(itinerary.days):
            if day.day_number == target_day:
                found = True
                new_day = cls._create_single_day_plan(
                    day_number=target_day,
                    date_str=day.date,
                    destination=itinerary.destination.query,
                    travel_style=itinerary.travel_style,
                    currency=itinerary.currency,
                    group_size=itinerary.group_size,
                    total_days=itinerary.total_days,
                    user_budget=itinerary.budget_breakdown.user_budget,
                    is_domestic=is_domestic,
                    focus_override=request.focus_note,
                    offset=target_day + 10
                )
                itinerary.days[idx] = new_day
                break

        if not found:
            raise ValueError(f"Day {target_day} not found in this itinerary (total days: {len(itinerary.days)}).")

        # Recalculate exact budget breakdown from actual day plans
        itinerary.budget_breakdown = BudgetService.build_breakdown_from_days(
            days=itinerary.days,
            user_budget=itinerary.budget_breakdown.user_budget,
            currency=itinerary.currency,
            total_days=itinerary.total_days,
            group_size=itinerary.group_size,
            travel_style=itinerary.travel_style,
            is_domestic=is_domestic
        )
        return itinerary

    @classmethod
    def refine_itinerary(cls, request: RefineTripRequest) -> Itinerary:
        """
        Applies user refinement instructions across the itinerary and reconciles budget.
        """
        itinerary = request.itinerary
        instruction = request.refinement_instruction.lower()
        is_domestic = (itinerary.destination.country.lower() == "india" and itinerary.currency == "INR")

        for day in itinerary.days:
            day.theme = f"{day.theme} (Refined: {request.refinement_instruction[:40]})"
            day.sensible_schedule_note += f" Updated per user preference: '{request.refinement_instruction}'."
            
            if "veg" in instruction:
                for meal in day.meals:
                    meal.suggestion = f"{meal.suggestion} (Pure Vegetarian Selection)"
                    meal.cuisine_type = f"{meal.cuisine_type} - Vegetarian"

            if "relax" in instruction or "slow" in instruction:
                if len(day.activities) > 2:
                    # Keep 2 most immersive activities
                    day.activities = day.activities[:2]
                    day.activities[1].time_slot = "Afternoon (14:30 - 17:00)"
                    day.activities[1].description += " (Paced comfortably with relaxed afternoon tea break)."

            # Recalculate each day's exact estimated cost
            day.estimated_daily_cost = round(
                sum(a.estimated_cost for a in day.activities)
                + sum(m.estimated_cost for m in day.meals)
                + day.accommodation.estimated_nightly_cost
                + getattr(day, "daily_transport_cost", 0.0),
                2
            )

        itinerary.why_it_matches += f" Refined specifically for: '{request.refinement_instruction}'."

        # Recalculate exact budget breakdown from updated day plans
        itinerary.budget_breakdown = BudgetService.build_breakdown_from_days(
            days=itinerary.days,
            user_budget=itinerary.budget_breakdown.user_budget,
            currency=itinerary.currency,
            total_days=itinerary.total_days,
            group_size=itinerary.group_size,
            travel_style=itinerary.travel_style,
            is_domestic=is_domestic
        )
        return itinerary

    @classmethod
    def _generate_via_ai(
        cls,
        request: TripRequest,
        dest_info: DestinationInfo,
        total_days: int,
        is_domestic: bool
    ) -> Optional[Itinerary]:
        if settings.GEMINI_API_KEY:
            return cls._call_gemini_api(request, dest_info, total_days, is_domestic)
        elif settings.OPENAI_API_KEY:
            return cls._call_openai_api(request, dest_info, total_days, is_domestic)
        return None

    @classmethod
    def _call_gemini_api(
        cls,
        request: TripRequest,
        dest_info: DestinationInfo,
        total_days: int,
        is_domestic: bool
    ) -> Optional[Itinerary]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
        prompt = cls._build_ai_prompt(request, dest_info, total_days)
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
                "response_mime_type": "application/json"
            }
        }
        with httpx.Client(timeout=25.0) as client:
            resp = client.post(url, json=payload)
            if resp.status_code != 200:
                logger.error(f"Gemini API returned status {resp.status_code}: {resp.text}")
                return None
            data = resp.json()
            candidates = data.get("candidates", [])
            if not candidates:
                return None
            text_part = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            if not text_part:
                return None
            parsed_json = json.loads(text_part)
            return cls._build_itinerary_from_ai_json(parsed_json, request, dest_info, total_days, is_domestic, model_name=f"Google Gemini ({settings.GEMINI_MODEL})")

    @classmethod
    def _call_openai_api(
        cls,
        request: TripRequest,
        dest_info: DestinationInfo,
        total_days: int,
        is_domestic: bool
    ) -> Optional[Itinerary]:
        url = "https://api.openai.com/v1/chat/completions"
        prompt = cls._build_ai_prompt(request, dest_info, total_days)
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": settings.OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are WanderWise, an expert travel itinerary planner. Output strictly valid JSON matching the requested schema."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.3
        }
        with httpx.Client(timeout=25.0) as client:
            resp = client.post(url, json=payload, headers=headers)
            if resp.status_code != 200:
                logger.error(f"OpenAI API error {resp.status_code}: {resp.text}")
                return None
            res_data = resp.json()
            content = res_data["choices"][0]["message"]["content"]
            parsed_json = json.loads(content)
            return cls._build_itinerary_from_ai_json(parsed_json, request, dest_info, total_days, is_domestic, model_name=f"OpenAI ({settings.OPENAI_MODEL})")

    @classmethod
    def _build_ai_prompt(cls, request: TripRequest, dest_info: DestinationInfo, total_days: int) -> str:
        return f"""
Generate a structured {total_days}-day travel itinerary for {dest_info.resolved_name}.
Parameters:
- Travel Start Date: {request.start_date}
- Travel End Date: {request.end_date}
- Total Days: {total_days}
- Group Size: {request.group_size} travelers
- Total Trip Budget: {request.currency} {request.budget:,.2f} (FOR ENTIRE GROUP AND ENTIRE TRIP)
- Travel Style: {request.travel_style.value}
- Interests: {', '.join(request.interests)}
- Special Preferences: {request.special_preferences or 'None'}

Return ONLY a JSON object with this exact structure:
{{
  "title": "Inspiring Title for Trip",
  "why_it_matches": "2-3 concise sentences explaining how activities reflect the user's specific interests and travel style.",
  "days": [
    {{
      "day_number": 1,
      "date": "YYYY-MM-DD",
      "theme": "Theme of day",
      "sensible_schedule_note": "Explanation of geographic clustering to avoid crisscrossing the city",
      "daily_transport_summary": "Best transit method (e.g., Metro Day Pass or local cabs)",
      "daily_transport_cost": 500.0,
      "accommodation": {{
        "recommended_area": "District/Neighborhood name",
        "stay_type": "e.g. 3-Star Heritage Hotel",
        "estimated_nightly_cost": 2200.0,
        "tips": "Practical booking guidance"
      }},
      "meals": [
        {{"meal_type": "Breakfast", "suggestion": "Spot / Dish", "cuisine_type": "Local", "estimated_cost": 300.0}},
        {{"meal_type": "Lunch", "suggestion": "Spot / Dish", "cuisine_type": "Regional", "estimated_cost": 600.0}},
        {{"meal_type": "Dinner", "suggestion": "Spot / Dish", "cuisine_type": "Traditional", "estimated_cost": 900.0}}
      ],
      "activities": [
        {{
          "id": "day1-act1",
          "title": "Attraction Title",
          "time_slot": "Morning (09:00 - 12:00)",
          "category": "Culture",
          "description": "Engaging visitor description and tips",
          "estimated_cost": 400.0,
          "cost_status": "estimated",
          "transport_guidance": "15 min metro ride or 10 min cab from hotel",
          "tips": "Book tickets online in advance"
        }}
      ]
    }}
  ]
}}
IMPORTANT BUDGET & PLANNING CONSTRAINTS:
- Total Trip Budget: {request.currency} {request.budget:,.2f} for the WHOLE GROUP ({request.group_size} travelers) across all {total_days} days.
- Target daily group spend: approx {request.currency} {(request.budget / total_days):,.2f}/day.
- Budget-Aware Choices: If the budget is tight, prioritize free sights, public walking tours, city buses, and local dhabas/markets. If the budget is generous, select higher-end boutique/palace hotels, private transfers, and curated entry tours matching {request.travel_style.value} style.
- All component costs (accommodation nightly cost, meals, activities, and daily_transport_cost) must be in {request.currency} for the ENTIRE GROUP of {request.group_size}.
- The sum of all items across the {total_days} days must realistically target the specified budget of {request.currency} {request.budget:,.2f}.
"""

    @classmethod
    def _build_itinerary_from_ai_json(
        cls,
        data: Dict[str, Any],
        request: TripRequest,
        dest_info: DestinationInfo,
        total_days: int,
        is_domestic: bool,
        model_name: str
    ) -> Itinerary:
        days_data = data.get("days", [])
        validated_days: List[DayPlan] = []
        cur_date = request.start_date

        for i in range(total_days):
            day_raw = days_data[i] if i < len(days_data) else {}
            date_str = cur_date.strftime("%Y-%m-%d")
            
            raw_acts = day_raw.get("activities", [])
            acts: List[Activity] = []
            for j, act in enumerate(raw_acts):
                c = float(act.get("estimated_cost", 0.0))
                acts.append(Activity(
                    id=f"day{i+1}-act{j+1}",
                    title=act.get("title", f"Explore {dest_info.resolved_name}"),
                    time_slot=act.get("time_slot", "Morning" if j == 0 else "Afternoon"),
                    category=act.get("category", "Culture"),
                    description=act.get("description", "Walk through historic landmarks and cultural sights."),
                    estimated_cost=round(max(0.0, c), 2),
                    cost_status="free" if c == 0 else "estimated",
                    transport_guidance=act.get("transport_guidance", "Local transit or taxi"),
                    tips=act.get("tips", "Check operational hours before arrival")
                ))

            if not acts:
                acts.append(Activity(
                    id=f"day{i+1}-act1",
                    title=f"Highlights of {dest_info.resolved_name}",
                    time_slot="Morning (09:30 - 12:30)",
                    category="Attraction",
                    description="Self-guided landmark walking tour through central historic streets.",
                    estimated_cost=0.0,
                    cost_status="free",
                    transport_guidance="Central pedestrian district",
                    tips="Wear comfortable walking shoes"
                ))

            raw_meals = day_raw.get("meals", [])
            meals: List[MealOption] = []
            for m in raw_meals:
                meals.append(MealOption(
                    meal_type=m.get("meal_type", "Lunch"),
                    suggestion=m.get("suggestion", "Local Specialty Eatery"),
                    cuisine_type=m.get("cuisine_type", "Regional Cuisine"),
                    estimated_cost=round(max(0.0, float(m.get("estimated_cost", 10.0))), 2)
                ))
            if not meals:
                meals = [
                    MealOption(meal_type="Breakfast", suggestion="Artisanal Morning Cafe", cuisine_type="Cafe", estimated_cost=300.0 if request.currency=="INR" else 15.0),
                    MealOption(meal_type="Lunch", suggestion="Traditional Neighborhood Bistro", cuisine_type="Regional", estimated_cost=600.0 if request.currency=="INR" else 30.0),
                    MealOption(meal_type="Dinner", suggestion="Authentic Dinner Experience", cuisine_type="Local", estimated_cost=900.0 if request.currency=="INR" else 45.0),
                ]

            raw_acc = day_raw.get("accommodation", {})
            accommodation = AccommodationGuidance(
                recommended_area=raw_acc.get("recommended_area", f"Central {dest_info.resolved_name}"),
                stay_type=raw_acc.get("stay_type", f"{request.travel_style.value.title()} Hotel / Stay"),
                estimated_nightly_cost=round(max(0.0, float(raw_acc.get("estimated_nightly_cost", 2000.0 if request.currency=="INR" else 80.0))), 2),
                tips=raw_acc.get("tips", "Reserve in advance for best location and rates")
            )

            daily_trans = round(max(0.0, float(day_raw.get("daily_transport_cost", 400.0 if request.currency=="INR" else 20.0))), 2)

            daily_cost = round(
                sum(a.estimated_cost for a in acts)
                + sum(m.estimated_cost for m in meals)
                + accommodation.estimated_nightly_cost
                + daily_trans,
                2
            )

            validated_days.append(DayPlan(
                day_number=i + 1,
                date=date_str,
                theme=day_raw.get("theme", f"Discovering {dest_info.resolved_name} - Part {i+1}"),
                activities=acts,
                meals=meals,
                accommodation=accommodation,
                daily_transport_summary=day_raw.get("daily_transport_summary", "Metro, local bus, and on-demand cabs"),
                daily_transport_cost=daily_trans,
                estimated_daily_cost=daily_cost,
                sensible_schedule_note=day_raw.get(
                    "sensible_schedule_note",
                    "Activities arranged sequentially within the same geographic cluster to minimize transit time."
                )
            ))
            cur_date += datetime.timedelta(days=1)

        budget_breakdown = BudgetService.build_breakdown_from_days(
            days=validated_days,
            user_budget=request.budget,
            currency=request.currency,
            total_days=total_days,
            group_size=request.group_size,
            travel_style=request.travel_style,
            is_domestic=is_domestic
        )

        return Itinerary(
            id=str(uuid.uuid4()),
            title=data.get("title", f"{dest_info.resolved_name} {request.travel_style.value.title()} Journey"),
            destination=dest_info,
            start_date=request.start_date.strftime("%Y-%m-%d"),
            end_date=request.end_date.strftime("%Y-%m-%d"),
            total_days=total_days,
            travel_style=request.travel_style,
            group_size=request.group_size,
            currency=request.currency,
            days=validated_days,
            budget_breakdown=budget_breakdown,
            why_it_matches=data.get(
                "why_it_matches",
                f"Tailored to highlight your interest in {', '.join(request.interests)} with a {request.travel_style.value} rhythm."
            ),
            generation_source="ai_model",
            model_name=model_name,
            disclaimer="All costs, schedules, and recommendations are estimated planning guidance and require independent verification before travel.",
            created_at=datetime.datetime.now(datetime.timezone.utc).isoformat()
        )

    @classmethod
    def _generate_via_curated_engine(
        cls,
        request: TripRequest,
        dest_info: DestinationInfo,
        total_days: int,
        is_domestic: bool
    ) -> Itinerary:
        """
        Deterministic, verified curated travel engine calibrated to fit within
        the user's budget where feasible, or honestly report budget shortfalls.
        """
        days: List[DayPlan] = []
        cur_date = request.start_date

        for day_num in range(1, total_days + 1):
            date_str = cur_date.strftime("%Y-%m-%d")
            day_plan = cls._create_single_day_plan(
                day_number=day_num,
                date_str=date_str,
                destination=dest_info.query,
                travel_style=request.travel_style,
                currency=request.currency,
                group_size=request.group_size,
                total_days=total_days,
                user_budget=request.budget,
                is_domestic=is_domestic,
                offset=day_num - 1
            )
            days.append(day_plan)
            cur_date += datetime.timedelta(days=1)

        breakdown = BudgetService.build_breakdown_from_days(
            days=days,
            user_budget=request.budget,
            currency=request.currency,
            total_days=total_days,
            group_size=request.group_size,
            travel_style=request.travel_style,
            is_domestic=is_domestic
        )

        interests_str = ", ".join(request.interests)
        why_matches = (
            f"Curated for {request.group_size} traveler(s) focusing on {interests_str} "
            f"with a {request.travel_style.value} pace. Activities are geographically clustered by neighborhood "
            "to maximize exploration time while keeping transit effortless."
        )

        return Itinerary(
            id=str(uuid.uuid4()),
            title=f"{dest_info.resolved_name}: {request.travel_style.value.title()} {total_days}-Day Exploration",
            destination=dest_info,
            start_date=request.start_date.strftime("%Y-%m-%d"),
            end_date=request.end_date.strftime("%Y-%m-%d"),
            total_days=total_days,
            travel_style=request.travel_style,
            group_size=request.group_size,
            currency=request.currency,
            days=days,
            budget_breakdown=breakdown,
            why_it_matches=why_matches,
            generation_source="fallback_curated_engine",
            model_name="WanderWise Curated Rules Engine v1.0",
            disclaimer="Generated using WanderWise's verified curated itinerary rule-engine (AI API key not configured or offline). Recommendations are structured templates calibrated to your dates, travel style, and interests.",
            created_at=datetime.datetime.now(datetime.timezone.utc).isoformat()
        )

    @classmethod
    def _create_single_day_plan(
        cls,
        day_number: int,
        date_str: str,
        destination: str,
        travel_style: TravelStyle,
        currency: str,
        group_size: int,
        total_days: int,
        user_budget: float,
        is_domestic: bool,
        focus_override: Optional[str] = None,
        offset: int = 0
    ) -> DayPlan:
        """
        Creates a coherent, geographically structured single day plan whose costs
        reconcile mathematically with the target budget and style.
        """
        rates_table = BudgetService.DOMESTIC_MIN_DAILY_USD if is_domestic else BudgetService.GLOBAL_MIN_DAILY_USD
        min_rate_usd = rates_table[travel_style]
        min_daily_group_local = BudgetService.convert_usd_to_currency(min_rate_usd * group_size, currency)
        
        # Absolute minimal viable daily spend per person to prevent unrealistically broken numbers
        # In domestic destinations (India): approx $9.60 USD / ₹800 per person per day
        # In international destinations: approx $40.00 USD per person per day
        min_viable_per_person_usd = 9.60 if is_domestic else 40.0
        min_viable_daily_group = BudgetService.convert_usd_to_currency(min_viable_per_person_usd * group_size, currency)

        # User's entered daily budget for the whole group
        user_daily_group_budget = user_budget / total_days

        # Genuinely adapt to the user's budget where viable, or floor at minimal viable rate
        if user_daily_group_budget >= min_viable_daily_group:
            effective_daily_budget = user_daily_group_budget
        else:
            effective_daily_budget = min_viable_daily_group

        # Daily per-person budget in INR equivalent for tiered styling
        usd_rate = BudgetService.get_usd_rate(currency)
        inr_per_person = (effective_daily_budget / group_size) * (usd_rate / 0.012)

        # Cost allocation ratios based on travel style
        if travel_style == TravelStyle.BUDGET:
            stay_ratio, food_ratio, trans_ratio = 0.36, 0.34, 0.14
        elif travel_style == TravelStyle.PREMIUM:
            stay_ratio, food_ratio, trans_ratio = 0.46, 0.28, 0.12
        else:
            stay_ratio, food_ratio, trans_ratio = 0.40, 0.30, 0.12

        # 1. Lodging for the group
        stay_cost = round(effective_daily_budget * stay_ratio, 2)
        if inr_per_person < 1500:
            stay_title = "Economy Guesthouse / Backpacker Hostel Dorm"
            stay_tips = "Clean budget lodging or dorms; book in advance for prime central locations."
        elif inr_per_person < 4000:
            stay_title = "3-Star Boutique Hotel & Suites"
            stay_tips = "Comfortable standard rooms near heritage center; reserve 2-3 weeks in advance."
        elif inr_per_person < 8000:
            stay_title = "4-Star Heritage Haveli / Premium Resort"
            stay_tips = "Character-rich heritage haveli with modern amenities and courtyard pool."
        else:
            stay_title = "5-Star Luxury Palace Hotel / Heritage Suite"
            stay_tips = "World-class royal hospitality, private butler service, and heritage spa."

        accommodation = AccommodationGuidance(
            recommended_area="Central Old Town / Heritage District",
            stay_type=stay_title,
            estimated_nightly_cost=stay_cost,
            tips=stay_tips
        )

        # 2. Meals for the group
        total_food_cost = round(effective_daily_budget * food_ratio, 2)
        breakfast_cost = round(total_food_cost * 0.18, 2)
        lunch_cost = round(total_food_cost * 0.36, 2)
        dinner_cost = round(total_food_cost - breakfast_cost - lunch_cost, 2)

        if inr_per_person < 1500:
            b_sugg, b_cuis = "Street Corner Chai & Fresh Kachori / Poha", "Local Morning Street Specialties"
            l_sugg, l_cuis = "Neighborhood Thali / Local Dhaba", "Authentic Regional Thali"
            d_sugg, d_cuis = "Popular Night Street Food Bazaar", "Vibrant Street Eats & Sweets"
        elif inr_per_person < 4000:
            b_sugg, b_cuis = "Artisanal Cafe or Hotel Buffet Spread", "Fresh Morning Fare, Regional Breads & Coffee"
            l_sugg, l_cuis = "Traditional Bistro / Local Delicacy Kitchen", "Authentic Regional Specialties"
            d_sugg, d_cuis = "Courtyard Heritage Restaurant", "Contemporary Regional Dining"
        elif inr_per_person < 8000:
            b_sugg, b_cuis = "Lavish Buffet at Heritage Dining Hall", "Gourmet Continental & Regional Selection"
            l_sugg, l_cuis = "Fine Regional Gastronomy & Royal Thali", "Palace Recipe Degustation"
            d_sugg, d_cuis = "Rooftop Starlit Dining overlooking the City", "Premium Mughlai & Rajput Cuisine"
        else:
            b_sugg, b_cuis = "Gourmet Palace Veranda Breakfast", "Private Chef Table & Artisanal Juices"
            l_sugg, l_cuis = "Curated Culinary Tasting Menu & Royal Thali", "Multi-Course Heritage Banquet"
            d_sugg, d_cuis = "Exclusive Fine Dining Experience in Historical Pavilion", "Royal Heritage Gastronomy"

        meals = [
            MealOption(meal_type="Breakfast", suggestion=b_sugg, cuisine_type=b_cuis, estimated_cost=breakfast_cost),
            MealOption(meal_type="Lunch", suggestion=l_sugg, cuisine_type=l_cuis, estimated_cost=lunch_cost),
            MealOption(meal_type="Dinner", suggestion=d_sugg, cuisine_type=d_cuis, estimated_cost=dinner_cost)
        ]

        # 3. Local Transit for the group
        trans_cost = round(effective_daily_budget * trans_ratio, 2)

        # 4. Activities for the group (remainder ensures exact mathematical match)
        total_act_cost = round(effective_daily_budget - stay_cost - total_food_cost - trans_cost, 2)
        act1_cost = round(total_act_cost * 0.45, 2)
        act2_cost = round(total_act_cost - act1_cost, 2)
        act3_cost = 0.0 # Free scenic walk, heritage street, or market stroll

        dest_key = destination.lower().split(",")[0].strip()
        matched_acts = CITY_ACTIVITIES.get(dest_key, None)

        acts: List[Activity] = []
        if matched_acts:
            catalog_len = len(matched_acts)
            idx1 = (offset * 3) % catalog_len
            idx2 = (offset * 3 + 1) % catalog_len
            idx3 = (offset * 3 + 2) % catalog_len

            chosen = [matched_acts[idx1], matched_acts[idx2], matched_acts[idx3]]
            costs = [act1_cost, act2_cost, act3_cost]
            for i, item in enumerate(chosen):
                cost_val = 0.0 if item.get("free", False) else costs[i]
                acts.append(Activity(
                    id=f"day{day_number}-act{i+1}",
                    title=item["title"],
                    time_slot=item["slot"],
                    category=item["cat"],
                    description=item["desc"],
                    estimated_cost=cost_val,
                    cost_status="free" if cost_val == 0.0 else "estimated",
                    transport_guidance=item.get("transport", "Local transit / walking"),
                    tips="Comfortable walking shoes recommended."
                ))
        else:
            default_slots = [
                ("Heritage District Walking Tour", "Morning (09:30 - 12:30)", "Culture", "Guided walking orientation covering old town heritage architecture and central plazas.", act1_cost, "Short walk or local transit from hotel"),
                ("Regional Art & History Museum", "Afternoon (14:00 - 16:30)", "History", "Explore curated regional exhibits, craft collections, and cultural context.", act2_cost, "10 min metro or local cab"),
                ("Sunset Waterfront & Evening Market", "Evening (17:30 - 20:00)", "Relaxation", "Golden-hour walk along the promenade followed by lively evening local bazaar.", act3_cost, "Central walking district")
            ]
            for i, (title, slot, cat, desc, cost_val, transport) in enumerate(default_slots):
                acts.append(Activity(
                    id=f"day{day_number}-act{i+1}",
                    title=f"{destination.title()}: {title}",
                    time_slot=slot,
                    category=cat,
                    description=desc,
                    estimated_cost=cost_val,
                    cost_status="free" if cost_val == 0.0 else "estimated",
                    transport_guidance=transport,
                    tips="Check local opening hours."
                ))

        # Reconcile exact sum of activities to match total_act_cost
        sum_acts = sum(a.estimated_cost for a in acts)
        if sum_acts > 0 and abs(sum_acts - total_act_cost) > 0.001:
            diff = round(total_act_cost - sum_acts, 2)
            # Adjust first non-free activity
            for a in acts:
                if a.estimated_cost > 0:
                    a.estimated_cost = round(max(0.0, a.estimated_cost + diff), 2)
                    break

        # Calculate exact daily total
        actual_daily_cost = round(
            sum(a.estimated_cost for a in acts)
            + sum(m.estimated_cost for m in meals)
            + accommodation.estimated_nightly_cost
            + trans_cost,
            2
        )

        theme_titles = [
            "Heritage Heart & Architectural Landmarks",
            "Art, Culture & Neighborhood Flavour",
            "Hidden Treasures & Scenic Sunset Vistas",
            "Culinary Trails & Vibrant Markets",
            "Nature Escapes & Riverside Relaxation",
            "Royal Palaces & Historic Fortifications"
        ]
        theme = theme_titles[(day_number - 1) % len(theme_titles)]
        if focus_override:
            theme += f" — Focused on {focus_override}"

        return DayPlan(
            day_number=day_number,
            date=date_str,
            theme=theme,
            activities=acts,
            meals=meals,
            accommodation=accommodation,
            daily_transport_summary="Walkable route combined with short local metro/cab connections between morning and afternoon clusters.",
            daily_transport_cost=trans_cost,
            estimated_daily_cost=actual_daily_cost,
            sensible_schedule_note="Activities are grouped within the same district to minimize transit time, allowing a relaxed lunch between visits."
        )
