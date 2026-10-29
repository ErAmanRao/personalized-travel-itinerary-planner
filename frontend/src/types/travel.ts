export type TravelStyle = 'budget' | 'balanced' | 'premium';

export interface TripRequest {
  destination: string;
  start_date: string; // YYYY-MM-DD
  end_date: string;   // YYYY-MM-DD
  budget: number;
  currency: string;
  interests: string[];
  travel_style: TravelStyle;
  group_size: number;
  special_preferences?: string;
}

export interface DestinationInfo {
  query: string;
  resolved_name: string;
  country: string;
  latitude?: number | null;
  longitude?: number | null;
  verified: boolean;
  verification_source: string;
  image_url?: string | null;
  image_source?: string | null;
  photographer_name?: string | null;
  photographer_url?: string | null;
  image_attribution?: string | null;
  image_status?: 'verified' | 'api_result' | 'unavailable';
}

export interface Activity {
  id: string;
  title: string;
  time_slot: string;
  category: string;
  description: string;
  estimated_cost: number;
  cost_status: string;
  transport_guidance?: string | null;
  tips?: string | null;
}

export interface MealOption {
  meal_type: string;
  suggestion: string;
  cuisine_type: string;
  estimated_cost: number;
}

export interface AccommodationGuidance {
  recommended_area: string;
  stay_type: string;
  estimated_nightly_cost: number;
  tips: string;
}

export interface DayPlan {
  day_number: number;
  date: string;
  theme: string;
  activities: Activity[];
  meals: MealOption[];
  accommodation: AccommodationGuidance;
  daily_transport_summary: string;
  daily_transport_cost?: number;
  estimated_daily_cost: number;
  sensible_schedule_note: string;
}

export interface BudgetBreakdown {
  currency: string;
  currency_symbol: string;
  activities_cost: number;
  food_cost: number;
  accommodation_cost: number;
  local_transport_cost: number;
  total_estimated_cost: number;
  cost_per_person: number;
  user_budget: number;
  cost_type: string;
  budget_status: 'within_budget' | 'tight_budget' | 'budget_alert' | 'exceeds_budget';
  is_realistic: boolean;
  recommended_minimum_budget?: number | null;
  budget_analysis_notes: string;
}

export interface Itinerary {
  id: string;
  title: string;
  destination: DestinationInfo;
  start_date: string;
  end_date: string;
  total_days: number;
  travel_style: TravelStyle;
  group_size: number;
  currency: string;
  days: DayPlan[];
  budget_breakdown: BudgetBreakdown;
  why_it_matches: string;
  generation_source: string;
  model_name?: string | null;
  disclaimer: string;
  created_at: string;
}

export interface TripSummary {
  id: string;
  title: string;
  destination_name: string;
  country: string;
  start_date: string;
  end_date: string;
  total_days: number;
  travel_style: string;
  group_size: number;
  currency: string;
  total_estimated_cost: number;
  created_at: string;
  image_url?: string | null;
}

export interface BackendHealth {
  status: string;
  app_name: string;
  version: string;
  ai_engine: {
    configured: boolean;
    provider: string;
    fallback_engine: string;
  };
  database: {
    configured: boolean;
    mode: 'supabase_database' | 'preview_in_memory';
    message: string;
  };
}
