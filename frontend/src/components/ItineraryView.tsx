import React, { useState } from 'react';
import {
  Calendar,
  Wallet,
  Users,
  Compass,
  Sparkles,
  Bookmark,
  Sliders,
  RefreshCw,
  Navigation,
  Hotel,
  Utensils,
  AlertTriangle,
  Info,
  CheckCircle2,
  Clock,
  MapPin,
  ChevronRight
} from 'lucide-react';
import { Itinerary, Activity, DayPlan } from '../types/travel';
import { formatDate } from '../utils/dates';
import { formatCurrency } from '../utils/currency';
import { ActivityCard } from './ActivityCard';
import { BudgetBreakdownCard } from './BudgetBreakdownCard';
import { EditActivityModal } from './EditActivityModal';
import { RegenerateDayModal } from './RegenerateDayModal';
import { RefineTripModal } from './RefineTripModal';
import { DestinationPhotoCard } from './DestinationPhotoCard';

interface ItineraryViewProps {
  itinerary: Itinerary;
  onUpdateActivity: (dayNumber: number, activity: Activity) => void;
  onRegenerateDay: (dayNumber: number, focusNote?: string) => void;
  onRefineTrip: (instruction: string) => void;
  onSaveTrip: () => void;
  onPlanNew: () => void;
  isSaving: boolean;
  isRegenerating: boolean;
  isRefining: boolean;
  isSaved: boolean;
}

export const ItineraryView: React.FC<ItineraryViewProps> = ({
  itinerary,
  onUpdateActivity,
  onRegenerateDay,
  onRefineTrip,
  onSaveTrip,
  onPlanNew,
  isSaving,
  isRegenerating,
  isRefining,
  isSaved,
}) => {
  const [selectedDayTab, setSelectedDayTab] = useState<number | 'all'>('all');

  // Modal States
  const [editingActivity, setEditingActivity] = useState<{ activity: Activity; dayNumber: number } | null>(null);
  const [regeneratingDayNumber, setRegeneratingDayNumber] = useState<number | null>(null);
  const [isRefineModalOpen, setIsRefineModalOpen] = useState<boolean>(false);

  const destination = itinerary.destination;
  const breakdown = itinerary.budget_breakdown;

  const displayedDays =
    selectedDayTab === 'all'
      ? itinerary.days
      : itinerary.days.filter((d) => d.day_number === selectedDayTab);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 pb-24 space-y-8 animate-fade-in">
      {/* 1. EDITORIAL DESTINATION BANNER WITH FEATURED PHOTO HERO */}
      <div className="relative rounded-3xl overflow-hidden bg-midnight-950 text-white p-6 sm:p-10 shadow-soft-lg border border-white/10">
        <div className="relative z-10 flex flex-col lg:flex-row items-center gap-8 justify-between">
          {/* Left Column: Heading, Badges, Details, Actions */}
          <div className="flex-1 w-full flex flex-col justify-between space-y-6">
            {/* Top Badges & Action Bar */}
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-[11px] font-bold uppercase tracking-wider px-3 py-1 rounded-full bg-white/90 text-midnight-950 backdrop-blur-md shadow-soft-sm">
                  {itinerary.travel_style} Travel
                </span>
                <span className="text-[11px] font-bold uppercase tracking-wider px-3 py-1 rounded-full bg-wanderteal-950/80 text-wanderteal-300 border border-wanderteal-500/30 backdrop-blur-md">
                  {destination.verified ? 'Verified Destination' : 'Custom Query'}
                </span>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => setIsRefineModalOpen(true)}
                  className="px-3.5 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-semibold backdrop-blur-md border border-white/20 flex items-center gap-1.5 transition-colors"
                >
                  <Sliders className="w-3.5 h-3.5 text-sunset-400" />
                  <span>Refine</span>
                </button>

                <button
                  onClick={onSaveTrip}
                  disabled={isSaving || isSaved}
                  className={`px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all shadow-soft-sm ${
                    isSaved
                      ? 'bg-emerald-600 text-white cursor-default'
                      : 'bg-midnight-900 text-ivory-50 hover:bg-midnight-800 border border-white/20'
                  }`}
                >
                  {isSaved ? (
                    <>
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-200" />
                      <span>Saved</span>
                    </>
                  ) : (
                    <>
                      <Bookmark className="w-3.5 h-3.5 text-wanderteal-400" />
                      <span>{isSaving ? 'Saving...' : 'Save Trip'}</span>
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Headline Details */}
            <div className="pt-2">
              <span className="text-xs uppercase tracking-widest text-wanderteal-400 font-semibold flex items-center gap-1.5 mb-1.5">
                <MapPin className="w-3.5 h-3.5" />
                {destination.country}
              </span>
              <h1 className="font-editorial text-3xl sm:text-5xl font-bold text-white tracking-tight leading-tight mb-4">
                {destination.resolved_name}
              </h1>

              <div className="flex flex-wrap items-center gap-4 text-xs sm:text-sm text-ivory-200 font-medium">
                <span className="flex items-center gap-1.5">
                  <Calendar className="w-4 h-4 text-wanderteal-400" />
                  {formatDate(itinerary.start_date)} – {formatDate(itinerary.end_date)}
                </span>
                <span className="text-white/40">•</span>
                <span className="flex items-center gap-1.5">
                  <Clock className="w-4 h-4 text-wanderteal-400" />
                  {itinerary.total_days} {itinerary.total_days === 1 ? 'Day' : 'Days'}
                </span>
                <span className="text-white/40">•</span>
                <span className="flex items-center gap-1.5">
                  <Users className="w-4 h-4 text-wanderteal-400" />
                  {itinerary.group_size} {itinerary.group_size === 1 ? 'Traveler' : 'Travelers'}
                </span>
              </div>
            </div>
          </div>

          {/* Right Column: Featured Large Destination Photo Experience */}
          <div className="w-full lg:w-[440px] shrink-0">
            <DestinationPhotoCard destination={destination} />
          </div>
        </div>
      </div>

      {/* 2. SUMMARY METRICS ROW */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Metric 1: Total Estimate */}
        <div className="bg-white rounded-2xl p-4 sm:p-5 border border-ivory-200 shadow-soft-sm">
          <span className="text-[11px] font-bold uppercase tracking-wider text-midnight-500 block mb-1">
            Group Total Estimated Cost
          </span>
          <div className="font-editorial text-xl sm:text-2xl font-bold text-midnight-950">
            {formatCurrency(breakdown.total_estimated_cost, itinerary.currency)}
          </div>
          <span
            className={`inline-block mt-1 text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${
              breakdown.is_realistic && (breakdown.budget_status === 'within_budget' || breakdown.budget_status === 'tight_budget')
                ? 'bg-emerald-50 text-emerald-800'
                : 'bg-amber-50 text-amber-800'
            }`}
          >
            {breakdown.budget_status === 'budget_alert'
              ? 'Budget Gap Alert'
              : breakdown.budget_status === 'exceeds_budget'
              ? 'Exceeds Budget'
              : breakdown.budget_status === 'tight_budget'
              ? 'Tight Budget'
              : 'Within Budget'}
          </span>
        </div>

        {/* Metric 2: Per Person */}
        <div className="bg-white rounded-2xl p-4 sm:p-5 border border-ivory-200 shadow-soft-sm">
          <span className="text-[11px] font-bold uppercase tracking-wider text-midnight-500 block mb-1">
            Cost Per Traveler
          </span>
          <div className="font-editorial text-xl sm:text-2xl font-bold text-midnight-950">
            {formatCurrency(breakdown.cost_per_person, itinerary.currency)}
          </div>
          <span className="text-[11px] text-midnight-500 mt-1 block">
            {itinerary.total_days} days ({formatCurrency(breakdown.cost_per_person / itinerary.total_days, itinerary.currency)}/day)
          </span>
        </div>

        {/* Metric 3: Travel Rhythm */}
        <div className="bg-white rounded-2xl p-4 sm:p-5 border border-ivory-200 shadow-soft-sm">
          <span className="text-[11px] font-bold uppercase tracking-wider text-midnight-500 block mb-1">
            Pacing & Style
          </span>
          <div className="font-editorial text-xl sm:text-2xl font-bold capitalize text-midnight-950">
            {itinerary.travel_style}
          </div>
          <span className="text-[11px] text-midnight-500 mt-1 block">
            District-clustered sightseeing
          </span>
        </div>

        {/* Metric 4: Engine Origin Badge */}
        <div className="bg-white rounded-2xl p-4 sm:p-5 border border-ivory-200 shadow-soft-sm">
          <span className="text-[11px] font-bold uppercase tracking-wider text-midnight-500 block mb-1">
            Planner Engine
          </span>
          <div className="font-bold text-sm sm:text-base text-midnight-900 truncate">
            {itinerary.model_name || (itinerary.generation_source === 'ai_model' ? 'AI Generator' : 'Curated Rules Engine')}
          </div>
          <span className="text-[11px] text-wanderteal-700 font-semibold mt-1 block">
            {itinerary.generation_source === 'ai_model' ? 'Real AI Generation' : 'Curated Rule Engine'}
          </span>
        </div>
      </div>

      {/* 3. REALISTIC BUDGET WARNING BANNER (If flagged) */}
      {(!breakdown.is_realistic || breakdown.budget_status === 'exceeds_budget') && (
        <div className="p-5 rounded-3xl bg-amber-50 border border-amber-300 text-amber-950 shadow-soft-sm">
          <div className="flex items-start gap-3.5">
            <AlertTriangle className="w-6 h-6 text-amber-600 shrink-0 mt-0.5" />
            <div className="w-full">
              <h3 className="font-bold text-sm sm:text-base text-amber-900 mb-1">
                {!breakdown.is_realistic ? 'Budget Realism Warning' : 'Estimated Cost Exceeds Your Target Budget'}
              </h3>
              <p className="text-xs sm:text-sm text-amber-900/90 leading-relaxed mb-3">
                {breakdown.budget_analysis_notes}
              </p>
              <div className="flex flex-wrap items-center gap-2">
                <div className="inline-flex items-center gap-2 bg-white/90 border border-amber-300 px-3 py-1.5 rounded-xl text-xs font-semibold text-amber-900">
                  <span>Your Total Budget:</span>
                  <span className="font-extrabold text-sm">
                    {formatCurrency(breakdown.user_budget, itinerary.currency)}
                  </span>
                </div>
                <div className="inline-flex items-center gap-2 bg-white/90 border border-amber-300 px-3 py-1.5 rounded-xl text-xs font-semibold text-amber-900">
                  <span>Itinerary Estimated Total:</span>
                  <span className="font-extrabold text-sm">
                    {formatCurrency(breakdown.total_estimated_cost, itinerary.currency)}
                  </span>
                </div>
                {breakdown.recommended_minimum_budget && (
                  <div className="inline-flex items-center gap-2 bg-white/90 border border-amber-300 px-3 py-1.5 rounded-xl text-xs font-semibold text-amber-900">
                    <span>Realistic Minimum Baseline:</span>
                    <span className="font-extrabold text-sm">
                      {formatCurrency(breakdown.recommended_minimum_budget, itinerary.currency)}
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 4. WHY IT MATCHES YOUR PREFERENCES */}
      <div className="p-6 rounded-3xl bg-white border border-ivory-200 shadow-soft-sm">
        <div className="flex items-center gap-2 mb-2 text-xs font-bold uppercase tracking-wider text-wanderteal-700">
          <Sparkles className="w-4 h-4" />
          <span>Curator's Note</span>
        </div>
        <p className="text-xs sm:text-sm text-midnight-800 leading-relaxed italic font-serif">
          "{itinerary.why_it_matches}"
        </p>
      </div>

      {/* 5. DAY NAVIGATOR TABS */}
      <div className="flex items-center justify-between border-b border-ivory-200 pb-3">
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 max-w-full">
          <button
            onClick={() => setSelectedDayTab('all')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0 ${
              selectedDayTab === 'all'
                ? 'bg-midnight-900 text-ivory-50 shadow-soft-sm'
                : 'bg-ivory-100 text-midnight-700 hover:bg-ivory-200'
            }`}
          >
            All Days ({itinerary.total_days})
          </button>

          {itinerary.days.map((day) => {
            const isSelected = selectedDayTab === day.day_number;
            return (
              <button
                key={day.day_number}
                onClick={() => setSelectedDayTab(day.day_number)}
                className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all shrink-0 ${
                  isSelected
                    ? 'bg-midnight-900 text-ivory-50 shadow-soft-sm'
                    : 'bg-ivory-100 text-midnight-700 hover:bg-ivory-200'
                }`}
              >
                Day {day.day_number}
              </button>
            );
          })}
        </div>

        <button
          onClick={onPlanNew}
          className="hidden sm:inline-flex text-xs font-bold text-midnight-600 hover:text-midnight-950 transition-colors"
        >
          Plan Another Trip →
        </button>
      </div>

      {/* 6. DAY-BY-DAY ITINERARY CARDS */}
      <div className="space-y-8">
        {displayedDays.map((day) => (
          <div
            key={day.day_number}
            className="bg-ivory-100/50 rounded-3xl p-6 sm:p-8 border border-ivory-200/80 shadow-soft-sm space-y-6"
          >
            {/* Day Header */}
            <div className="flex flex-wrap items-center justify-between gap-4 border-b border-ivory-200 pb-4">
              <div className="flex items-center gap-3">
                <span className="w-10 h-10 rounded-2xl bg-midnight-900 text-white font-editorial text-lg font-bold flex items-center justify-center shadow-soft-sm shrink-0">
                  {day.day_number}
                </span>
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-editorial text-xl sm:text-2xl font-bold text-midnight-950">
                      {day.theme}
                    </h3>
                  </div>
                  <span className="text-xs text-midnight-500 font-medium">
                    {formatDate(day.date)} • Est. Day Spend: {formatCurrency(day.estimated_daily_cost, itinerary.currency)} (Group)
                    {itinerary.group_size > 1 && ` • ${formatCurrency(day.estimated_daily_cost / itinerary.group_size, itinerary.currency)} / traveler`}
                  </span>
                </div>
              </div>

              {/* Action: Regenerate This Day */}
              <button
                onClick={() => setRegeneratingDayNumber(day.day_number)}
                disabled={isRegenerating}
                className="px-3.5 py-2 rounded-xl bg-white border border-ivory-300 text-midnight-800 hover:bg-ivory-100 hover:border-ivory-400 text-xs font-bold flex items-center gap-1.5 transition-colors shadow-soft-sm"
              >
                <RefreshCw className="w-3.5 h-3.5 text-wanderteal-600" />
                <span>Regenerate Day {day.day_number}</span>
              </button>
            </div>

            {/* Schedule Note: District Clustering explanation */}
            <div className="flex items-start gap-2.5 p-3.5 rounded-2xl bg-wanderteal-50/60 border border-wanderteal-200/60 text-wanderteal-950 text-xs">
              <Navigation className="w-4 h-4 text-wanderteal-700 shrink-0 mt-0.5" />
              <p className="leading-relaxed">
                <strong>Schedule Logic:</strong> {day.sensible_schedule_note}
              </p>
            </div>

            {/* Lodging & Daily Transit Highlights */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Accommodation guidance */}
              <div className="p-4 rounded-2xl bg-white border border-ivory-200 shadow-soft-sm space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="flex items-center gap-1.5 font-bold uppercase tracking-wider text-midnight-700">
                    <Hotel className="w-3.5 h-3.5 text-wanderteal-600" />
                    Recommended Stay
                  </span>
                  <span className="font-bold text-midnight-900">
                    {formatCurrency(day.accommodation.estimated_nightly_cost, itinerary.currency)}/night
                  </span>
                </div>
                <h4 className="font-bold text-sm text-midnight-950">
                  {day.accommodation.stay_type} in {day.accommodation.recommended_area}
                </h4>
                <p className="text-xs text-midnight-600 leading-relaxed">
                  {day.accommodation.tips}
                </p>
              </div>

              {/* Daily Transit guidance */}
              <div className="p-4 rounded-2xl bg-white border border-ivory-200 shadow-soft-sm space-y-1.5">
                <span className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-midnight-700">
                  <Navigation className="w-3.5 h-3.5 text-sky-600" />
                  Transit Route Guidance
                </span>
                <p className="text-xs text-midnight-700 leading-relaxed pt-1">
                  {day.daily_transport_summary}
                </p>
              </div>
            </div>

            {/* Activities Chronological Flow */}
            <div className="space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-midnight-800">
                Day {day.day_number} Activities & Sightseeing
              </h4>
              <div className="grid grid-cols-1 gap-3">
                {day.activities.map((activity) => (
                  <ActivityCard
                    key={activity.id}
                    activity={activity}
                    currency={itinerary.currency}
                    onEdit={(act) => setEditingActivity({ activity: act, dayNumber: day.day_number })}
                  />
                ))}
              </div>
            </div>

            {/* Daily Meals Guidance */}
            <div className="space-y-3 pt-2">
              <h4 className="text-xs font-bold uppercase tracking-wider text-midnight-800 flex items-center gap-1.5">
                <Utensils className="w-3.5 h-3.5 text-sunset-600" />
                <span>Culinary & Meal Recommendations</span>
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {day.meals.map((meal, mIdx) => (
                  <div
                    key={mIdx}
                    className="p-3.5 rounded-2xl bg-white border border-ivory-200 shadow-soft-sm space-y-1"
                  >
                    <div className="flex items-center justify-between text-[11px]">
                      <span className="font-bold uppercase tracking-wider text-sunset-700">
                        {meal.meal_type}
                      </span>
                      <span className="font-bold text-midnight-800">
                        {formatCurrency(meal.estimated_cost, itinerary.currency)}
                      </span>
                    </div>
                    <h5 className="font-bold text-xs text-midnight-950">{meal.suggestion}</h5>
                    <p className="text-[11px] text-midnight-500">{meal.cuisine_type}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* 7. FULL BUDGET BREAKDOWN CARD */}
      <BudgetBreakdownCard
        breakdown={breakdown}
        groupSize={itinerary.group_size}
      />

      {/* 8. EDIT ACTIVITY MODAL */}
      <EditActivityModal
        isOpen={Boolean(editingActivity)}
        activity={editingActivity?.activity || null}
        dayNumber={editingActivity?.dayNumber || 1}
        currency={itinerary.currency}
        onClose={() => setEditingActivity(null)}
        onSave={onUpdateActivity}
      />

      {/* 9. REGENERATE DAY MODAL */}
      <RegenerateDayModal
        isOpen={Boolean(regeneratingDayNumber)}
        dayNumber={regeneratingDayNumber || 1}
        isLoading={isRegenerating}
        onClose={() => setRegeneratingDayNumber(null)}
        onConfirm={(dayNum, focusNote) => {
          onRegenerateDay(dayNum, focusNote);
          setRegeneratingDayNumber(null);
        }}
      />

      {/* 10. REFINE TRIP MODAL */}
      <RefineTripModal
        isOpen={isRefineModalOpen}
        isLoading={isRefining}
        onClose={() => setIsRefineModalOpen(false)}
        onConfirm={(instruction) => {
          onRefineTrip(instruction);
          setIsRefineModalOpen(false);
        }}
      />
    </div>
  );
};
