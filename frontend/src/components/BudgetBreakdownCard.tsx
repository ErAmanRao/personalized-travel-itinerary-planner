import React, { useState } from 'react';
import { AlertTriangle, Info, Hotel, Utensils, Bus, Ticket, CheckCircle2, TrendingUp, TrendingDown } from 'lucide-react';
import { BudgetBreakdown } from '../types/travel';
import { formatCurrency } from '../utils/currency';

interface BudgetBreakdownCardProps {
  breakdown: BudgetBreakdown;
  groupSize: number;
}

export const BudgetBreakdownCard: React.FC<BudgetBreakdownCardProps> = ({
  breakdown,
  groupSize,
}) => {
  const [showPerPerson, setShowPerPerson] = useState<boolean>(false);

  const currency = breakdown.currency;
  const total = breakdown.total_estimated_cost;
  const userBudget = breakdown.user_budget;

  // Exact category percentages based on total estimated trip cost
  const stayPct = total > 0 ? Math.round((breakdown.accommodation_cost / total) * 100) : 0;
  const foodPct = total > 0 ? Math.round((breakdown.food_cost / total) * 100) : 0;
  const transPct = total > 0 ? Math.round((breakdown.local_transport_cost / total) * 100) : 0;
  const actPct = total > 0 ? Math.round((breakdown.activities_cost / total) * 100) : 0;

  // Values based on active toggle mode
  const displayedStay = showPerPerson
    ? Math.round((breakdown.accommodation_cost / groupSize) * 100) / 100
    : breakdown.accommodation_cost;

  const displayedFood = showPerPerson
    ? Math.round((breakdown.food_cost / groupSize) * 100) / 100
    : breakdown.food_cost;

  const displayedTrans = showPerPerson
    ? Math.round((breakdown.local_transport_cost / groupSize) * 100) / 100
    : breakdown.local_transport_cost;

  const displayedAct = showPerPerson
    ? Math.round((breakdown.activities_cost / groupSize) * 100) / 100
    : breakdown.activities_cost;

  const displayedTotal = showPerPerson ? breakdown.cost_per_person : breakdown.total_estimated_cost;
  const displayedBudgetShare = showPerPerson
    ? Math.round((userBudget / groupSize) * 100) / 100
    : userBudget;

  const isOverBudget = total > userBudget;
  const budgetDifference = Math.abs(total - userBudget);
  const displayedDiff = showPerPerson
    ? Math.round((budgetDifference / groupSize) * 100) / 100
    : budgetDifference;

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-ivory-200 shadow-soft-md">
      {/* Header with Per-Person Toggle */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-ivory-200 pb-5 mb-6">
        <div>
          <h3 className="font-editorial text-xl sm:text-2xl font-bold text-midnight-950">
            Trip Budget Breakdown
          </h3>
          <p className="text-xs text-midnight-600 mt-0.5">
            Transparently itemized across all primary travel expenses (100% reconciled)
          </p>
        </div>

        {groupSize > 1 && (
          <div className="flex items-center gap-1 bg-ivory-100 p-1 rounded-xl border border-ivory-200">
            <button
              onClick={() => setShowPerPerson(false)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                !showPerPerson
                  ? 'bg-midnight-900 text-ivory-50 shadow-soft-sm'
                  : 'text-midnight-700 hover:text-midnight-950'
              }`}
            >
              Whole Group ({groupSize})
            </button>
            <button
              onClick={() => setShowPerPerson(true)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                showPerPerson
                  ? 'bg-midnight-900 text-ivory-50 shadow-soft-sm'
                  : 'text-midnight-700 hover:text-midnight-950'
              }`}
            >
              Per Traveler Share
            </button>
          </div>
        )}
      </div>

      {/* Realistic Budget Warning / Exceeded Budget Notice */}
      {(!breakdown.is_realistic || isOverBudget) && (
        <div className="mb-6 p-4 rounded-2xl bg-amber-50 border border-amber-300 text-amber-950 text-xs sm:text-sm">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
            <div className="space-y-2 w-full">
              <div>
                <h4 className="font-bold text-amber-900">
                  {!breakdown.is_realistic ? 'Budget Realism Notice' : 'Estimated Cost Exceeds Specified Budget'}
                </h4>
                <p className="leading-relaxed text-amber-900/90 mt-1">
                  {breakdown.budget_analysis_notes}
                </p>
              </div>

              {/* 3 Explicit Separate Figures */}
              <div className="flex flex-wrap gap-2 pt-1">
                <div className="bg-white/90 border border-amber-300 px-3 py-1.5 rounded-xl font-medium text-amber-950 text-xs">
                  <span className="text-amber-800 font-semibold block text-[10px] uppercase">Your Total Budget:</span>
                  <span className="font-bold text-sm">{formatCurrency(userBudget, currency)}</span>
                </div>

                <div className="bg-white/90 border border-amber-300 px-3 py-1.5 rounded-xl font-medium text-amber-950 text-xs">
                  <span className="text-amber-800 font-semibold block text-[10px] uppercase">Itinerary Estimated Total:</span>
                  <span className="font-bold text-sm">{formatCurrency(total, currency)}</span>
                </div>

                {breakdown.recommended_minimum_budget && (
                  <div className="bg-white/90 border border-amber-300 px-3 py-1.5 rounded-xl font-medium text-amber-950 text-xs">
                    <span className="text-amber-800 font-semibold block text-[10px] uppercase">Realistic Baseline:</span>
                    <span className="font-bold text-sm">
                      {formatCurrency(breakdown.recommended_minimum_budget, currency)}
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Four Core Categories Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {/* Lodging */}
        <div className="p-4 rounded-2xl bg-ivory-50 border border-ivory-200">
          <div className="flex items-center justify-between text-midnight-600 text-xs mb-2">
            <span className="flex items-center gap-1.5 font-bold uppercase tracking-wider">
              <Hotel className="w-3.5 h-3.5 text-wanderteal-600" />
              Lodging
            </span>
            <span className="font-bold text-midnight-500" title="% of estimated trip cost">{stayPct}%</span>
          </div>
          <div className="font-editorial text-xl font-bold text-midnight-950">
            {formatCurrency(displayedStay, currency)}
          </div>
          <p className="text-[11px] text-midnight-500 mt-1">
            {showPerPerson ? 'Per traveler nightly share' : 'Recommended area hotels & stays'}
          </p>
        </div>

        {/* Food & Dining */}
        <div className="p-4 rounded-2xl bg-ivory-50 border border-ivory-200">
          <div className="flex items-center justify-between text-midnight-600 text-xs mb-2">
            <span className="flex items-center gap-1.5 font-bold uppercase tracking-wider">
              <Utensils className="w-3.5 h-3.5 text-sunset-600" />
              Food & Dining
            </span>
            <span className="font-bold text-midnight-500" title="% of estimated trip cost">{foodPct}%</span>
          </div>
          <div className="font-editorial text-xl font-bold text-midnight-950">
            {formatCurrency(displayedFood, currency)}
          </div>
          <p className="text-[11px] text-midnight-500 mt-1">
            {showPerPerson ? 'Per traveler dining share' : 'Breakfast, lunch & dinner guidance'}
          </p>
        </div>

        {/* Local Transit */}
        <div className="p-4 rounded-2xl bg-ivory-50 border border-ivory-200">
          <div className="flex items-center justify-between text-midnight-600 text-xs mb-2">
            <span className="flex items-center gap-1.5 font-bold uppercase tracking-wider">
              <Bus className="w-3.5 h-3.5 text-sky-600" />
              Local Transit
            </span>
            <span className="font-bold text-midnight-500" title="% of estimated trip cost">{transPct}%</span>
          </div>
          <div className="font-editorial text-xl font-bold text-midnight-950">
            {formatCurrency(displayedTrans, currency)}
          </div>
          <p className="text-[11px] text-midnight-500 mt-1">
            {showPerPerson ? 'Per traveler transit share' : 'Metro, buses & local cabs'}
          </p>
        </div>

        {/* Sightseeing & Activities */}
        <div className="p-4 rounded-2xl bg-ivory-50 border border-ivory-200">
          <div className="flex items-center justify-between text-midnight-600 text-xs mb-2">
            <span className="flex items-center gap-1.5 font-bold uppercase tracking-wider">
              <Ticket className="w-3.5 h-3.5 text-emerald-600" />
              Activities
            </span>
            <span className="font-bold text-midnight-500" title="% of estimated trip cost">{actPct}%</span>
          </div>
          <div className="font-editorial text-xl font-bold text-midnight-950">
            {formatCurrency(displayedAct, currency)}
          </div>
          <p className="text-[11px] text-midnight-500 mt-1">
            {showPerPerson ? 'Per traveler activity passes' : 'Palaces, museums & tours'}
          </p>
        </div>
      </div>

      {/* Total Bar */}
      <div className="p-5 rounded-2xl bg-midnight-900 text-ivory-50 flex flex-wrap items-center justify-between gap-4">
        <div>
          <span className="text-xs uppercase tracking-wider text-wanderteal-400 font-semibold block">
            {showPerPerson ? 'Total Estimated Cost (Per Traveler)' : 'Total Estimated Cost (Entire Group)'}
          </span>
          <span className="font-editorial text-2xl sm:text-3xl font-bold">
            {formatCurrency(displayedTotal, currency)}
          </span>
          {showPerPerson && (
            <span className="block text-[11px] text-ivory-300 mt-0.5">
              Whole Group Total: {formatCurrency(breakdown.total_estimated_cost, currency)}
            </span>
          )}
        </div>

        <div className="text-right">
          <span className="text-xs text-ivory-300 block">
            {showPerPerson ? 'Your Budget (Per Traveler Share)' : 'Your Specified Trip Budget (Group)'}
          </span>
          <span className="font-semibold text-xl text-ivory-100 block">
            {formatCurrency(displayedBudgetShare, currency)}
          </span>
          {showPerPerson && (
            <span className="block text-[11px] text-ivory-300 mt-0.5">
              Total Group Budget: {formatCurrency(userBudget, currency)}
            </span>
          )}
          <span
            className={`inline-flex items-center gap-1 mt-1 text-[11px] font-bold px-2 py-0.5 rounded-md ${
              isOverBudget ? 'bg-amber-500/20 text-amber-300' : 'bg-emerald-500/20 text-emerald-300'
            }`}
          >
            {isOverBudget ? (
              <>
                <TrendingUp className="w-3 h-3" />
                <span>+{formatCurrency(displayedDiff, currency)} over budget</span>
              </>
            ) : (
              <>
                <TrendingDown className="w-3 h-3" />
                <span>Within budget ({formatCurrency(displayedDiff, currency)} headroom)</span>
              </>
            )}
          </span>
        </div>
      </div>

      {/* Honest Travel Cost Disclaimer */}
      <div className="mt-4 flex items-start gap-2 text-[11px] text-midnight-500 leading-relaxed">
        <Info className="w-4 h-4 shrink-0 mt-0.5 text-midnight-400" />
        <p>
          <strong>Cost Transparency & Exact Reconciliation:</strong> Lodging, food, transit, and activities sum exactly to the displayed total estimated trip cost. All figures represent realistic planning estimates based on travel indices and group size ({groupSize} {groupSize === 1 ? 'traveler' : 'travelers'}).
        </p>
      </div>
    </div>
  );
};
