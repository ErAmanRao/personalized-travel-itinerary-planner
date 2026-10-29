from typing import Tuple, List
from app.models.schemas import (
    BudgetBreakdown,
    TravelStyle,
    DayPlan,
    SUPPORTED_CURRENCIES
)


class BudgetService:
    # Baseline daily minimum costs in USD per person per day
    GLOBAL_MIN_DAILY_USD = {
        TravelStyle.BUDGET: 50.0,     # approx ₹4,166 / person / day
        TravelStyle.BALANCED: 120.0,  # approx ₹10,000 / person / day
        TravelStyle.PREMIUM: 280.0,   # approx ₹23,300 / person / day
    }

    DOMESTIC_MIN_DAILY_USD = {
        TravelStyle.BUDGET: 15.0,     # approx ₹1,250 / person / day
        TravelStyle.BALANCED: 30.0,   # approx ₹2,500 / person / day
        TravelStyle.PREMIUM: 80.0,    # approx ₹6,666 / person / day
    }

    @classmethod
    def get_currency_symbol(cls, currency_code: str) -> str:
        return SUPPORTED_CURRENCIES.get(currency_code, {}).get("symbol", "₹")

    @classmethod
    def get_usd_rate(cls, currency_code: str) -> float:
        # returns 1 unit of user currency in USD
        return SUPPORTED_CURRENCIES.get(currency_code, {}).get("usd_rate", 0.012)

    @classmethod
    def convert_usd_to_currency(cls, amount_usd: float, currency_code: str) -> float:
        rate = cls.get_usd_rate(currency_code)
        if rate <= 0:
            return amount_usd
        return round(amount_usd / rate, 2)

    @classmethod
    def convert_currency_to_usd(cls, amount: float, currency_code: str) -> float:
        rate = cls.get_usd_rate(currency_code)
        return amount * rate

    @classmethod
    def evaluate_budget(
        cls,
        user_budget: float,
        currency: str,
        total_days: int,
        group_size: int,
        travel_style: TravelStyle,
        is_domestic: bool = False
    ) -> Tuple[bool, str, float, str]:
        """
        Evaluates whether user budget is realistic.
        Returns (is_realistic, budget_status, recommended_minimum, analysis_note)
        """
        rates_table = cls.DOMESTIC_MIN_DAILY_USD if is_domestic else cls.GLOBAL_MIN_DAILY_USD
        min_rate_usd = rates_table[travel_style]
        min_total_usd = min_rate_usd * total_days * group_size
        recommended_minimum = cls.convert_usd_to_currency(min_total_usd, currency)

        user_daily_per_person = round(user_budget / (total_days * group_size), 2)
        symbol = cls.get_currency_symbol(currency)

        if user_budget < recommended_minimum * 0.70:
            is_realistic = False
            status = "budget_alert"
            note = (
                f"Budget Alert: Your specified budget of {symbol}{user_budget:,.0f} for {group_size} travelers "
                f"over {total_days} days (approx {symbol}{user_daily_per_person:,.0f}/day/traveler) is significantly lower "
                f"than the realistic baseline of approx {symbol}{recommended_minimum:,.0f} for {travel_style.value} travel. "
                "WanderWise has structured a cost-optimized itinerary utilizing free sights, local transit, and budget dining, "
                "but accommodation and daily expenses will require additional funds."
            )
        elif user_budget < recommended_minimum:
            is_realistic = True
            status = "tight_budget"
            note = (
                f"Tight Budget: {symbol}{user_budget:,.0f} ({symbol}{user_daily_per_person:,.0f}/day/traveler) "
                f"requires conscious spend management. Typical baseline for {travel_style.value} travel is approx {symbol}{recommended_minimum:,.0f}. "
                "The itinerary prioritizes high-value stays and authentic local dining."
            )
        elif user_budget > recommended_minimum * 2.2:
            is_realistic = True
            status = "within_budget"
            note = (
                f"Generous Budget: Your budget of {symbol}{user_budget:,.0f} easily accommodates high-quality "
                f"{travel_style.value} experiences, private transfers, and premium culinary choices."
            )
        else:
            is_realistic = True
            status = "within_budget"
            note = (
                f"Healthy Budget: Your budget of {symbol}{user_budget:,.0f} ({symbol}{user_daily_per_person:,.0f}/day/traveler) "
                f"comfortably supports {travel_style.value} lodging, meals, transit, and sightseeing "
                f"(baseline: approx {symbol}{recommended_minimum:,.0f})."
            )

        return is_realistic, status, recommended_minimum, note

    @classmethod
    def build_breakdown_from_days(
        cls,
        days: List[DayPlan],
        user_budget: float,
        currency: str,
        total_days: int,
        group_size: int,
        travel_style: TravelStyle,
        is_domestic: bool = False
    ) -> BudgetBreakdown:
        """
        Calculates exact mathematical budget breakdown from the actual activities,
        meals, accommodation, and transit across all days in the itinerary.
        Guarantees that categories sum exactly to total_estimated_cost and that
        cost_per_person = total_estimated_cost / group_size.
        """
        is_realistic, eval_status, rec_min, note = cls.evaluate_budget(
            user_budget=user_budget,
            currency=currency,
            total_days=total_days,
            group_size=group_size,
            travel_style=travel_style,
            is_domestic=is_domestic
        )

        act_cost = round(sum(sum(a.estimated_cost for a in d.activities) for d in days), 2)
        food_cost = round(sum(sum(m.estimated_cost for m in d.meals) for d in days), 2)
        stay_cost = round(sum(d.accommodation.estimated_nightly_cost for d in days), 2)
        trans_cost = round(sum(getattr(d, "daily_transport_cost", 0.0) for d in days), 2)

        total_est = round(act_cost + food_cost + stay_cost + trans_cost, 2)
        per_person = round(total_est / group_size, 2)

        # Determine budget status against user's actual entered budget
        if not is_realistic:
            final_status = "budget_alert"
        elif total_est > user_budget:
            final_status = "exceeds_budget"
        elif eval_status == "tight_budget":
            final_status = "tight_budget"
        else:
            final_status = "within_budget"

        return BudgetBreakdown(
            currency=currency,
            currency_symbol=cls.get_currency_symbol(currency),
            activities_cost=act_cost,
            food_cost=food_cost,
            accommodation_cost=stay_cost,
            local_transport_cost=trans_cost,
            total_estimated_cost=total_est,
            cost_per_person=per_person,
            user_budget=round(user_budget, 2),
            cost_type="estimated",
            budget_status=final_status,
            is_realistic=is_realistic,
            recommended_minimum_budget=rec_min,
            budget_analysis_notes=note
        )

    @classmethod
    def calculate_breakdown(
        cls,
        total_estimated_cost: float,
        user_budget: float,
        currency: str,
        total_days: int,
        group_size: int,
        travel_style: TravelStyle,
        is_domestic: bool = False
    ) -> BudgetBreakdown:
        """
        Calculates an exact reconciled breakdown from a given total estimated cost.
        Guarantees that categories sum exactly to total_estimated_cost and
        cost_per_person = total_estimated_cost / group_size.
        """
        is_realistic, eval_status, rec_min, note = cls.evaluate_budget(
            user_budget=user_budget,
            currency=currency,
            total_days=total_days,
            group_size=group_size,
            travel_style=travel_style,
            is_domestic=is_domestic
        )

        stay_cost = round(total_estimated_cost * 0.40, 2)
        food_cost = round(total_estimated_cost * 0.25, 2)
        trans_cost = round(total_estimated_cost * 0.15, 2)
        # Force exact penny match for activities remainder
        act_cost = round(total_estimated_cost - (stay_cost + food_cost + trans_cost), 2)

        per_person = round(total_estimated_cost / group_size, 2)

        if not is_realistic:
            final_status = "budget_alert"
        elif total_estimated_cost > user_budget:
            final_status = "exceeds_budget"
        elif eval_status == "tight_budget":
            final_status = "tight_budget"
        else:
            final_status = "within_budget"

        return BudgetBreakdown(
            currency=currency,
            currency_symbol=cls.get_currency_symbol(currency),
            activities_cost=act_cost,
            food_cost=food_cost,
            accommodation_cost=stay_cost,
            local_transport_cost=trans_cost,
            total_estimated_cost=total_estimated_cost,
            cost_per_person=per_person,
            user_budget=round(user_budget, 2),
            cost_type="estimated",
            budget_status=final_status,
            is_realistic=is_realistic,
            recommended_minimum_budget=rec_min,
            budget_analysis_notes=note
        )
