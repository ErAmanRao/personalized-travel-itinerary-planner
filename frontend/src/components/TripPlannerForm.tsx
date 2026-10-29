import React, { useState } from 'react';
import {
  MapPin,
  Calendar,
  Wallet,
  Users,
  Compass,
  ArrowRight,
  AlertCircle,
  Clock,
  Sparkles,
  Check
} from 'lucide-react';
import { TripRequest, TravelStyle } from '../types/travel';
import { getTodayString, getDefaultEndDate, calculateTripDays } from '../utils/dates';
import { CURRENCY_SYMBOLS } from '../utils/currency';
import { parseAndValidateBudget } from '../utils/validation';

interface TripPlannerFormProps {
  onSubmit: (request: TripRequest) => void;
  isLoading: boolean;
}

const POPULAR_DESTINATIONS = [
  'Jaipur, Rajasthan',
  'Goa',
  'Kerala (Kochi & Munnar)',
  'Paris, France',
  'Tokyo, Japan',
  'London, UK',
  'Rome, Italy',
  'Udaipur, Rajasthan',
];

const AVAILABLE_INTERESTS = [
  { id: 'culture', label: 'Culture & Heritage', icon: '🏛️' },
  { id: 'history', label: 'History', icon: '📜' },
  { id: 'food', label: 'Food & Culinary', icon: '🍜' },
  { id: 'nature', label: 'Nature & Parks', icon: '🌿' },
  { id: 'relaxation', label: 'Relaxation & Spa', icon: '☕' },
  { id: 'beaches', label: 'Beaches & Coastal', icon: '🏖️' },
  { id: 'shopping', label: 'Shopping & Bazaars', icon: '🛍️' },
  { id: 'adventure', label: 'Adventure & Treks', icon: '🧗' },
  { id: 'photography', label: 'Photography', icon: '📸' },
  { id: 'architecture', label: 'Architecture', icon: '🏰' },
  { id: 'nightlife', label: 'Nightlife', icon: '🍸' },
];

const TRAVEL_STYLES: Array<{
  id: TravelStyle;
  title: string;
  badge: string;
  desc: string;
  accommodation: string;
}> = [
  {
    id: 'budget',
    title: 'Budget',
    badge: 'Savvy & Social',
    desc: 'Value-driven choices, public transit, local street food & cafes.',
    accommodation: 'Hostels, guesthouses, or budget stays',
  },
  {
    id: 'balanced',
    title: 'Balanced',
    badge: 'Popular Choice',
    desc: 'Comfortable balance of boutique stays, authentic bistros & cabs.',
    accommodation: '3-star boutique hotels & stylish Airbnbs',
  },
  {
    id: 'premium',
    title: 'Premium',
    badge: 'Luxury & Comfort',
    desc: 'Signature luxury stays, fine dining, private transfers & private guides.',
    accommodation: '4-5 star luxury hotels & heritage resorts',
  },
];

export const TripPlannerForm: React.FC<TripPlannerFormProps> = ({ onSubmit, isLoading }) => {
  const today = getTodayString();
  const defaultEnd = getDefaultEndDate(3);

  const [destination, setDestination] = useState<string>('Jaipur');
  const [startDate, setStartDate] = useState<string>(today);
  const [endDate, setEndDate] = useState<string>(defaultEnd);
  const [budget, setBudget] = useState<string>('30000');
  const [currency, setCurrency] = useState<string>('INR');
  const [interests, setInterests] = useState<string[]>(['culture', 'history', 'food']);
  const [travelStyle, setTravelStyle] = useState<TravelStyle>('balanced');
  const [groupSize, setGroupSize] = useState<number>(2);
  const [specialPreferences, setSpecialPreferences] = useState<string>('');

  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  const tripDays = calculateTripDays(startDate, endDate);

  const toggleInterest = (id: string) => {
    if (interests.includes(id)) {
      if (interests.length > 1) {
        setInterests(interests.filter((i) => i !== id));
      }
    } else {
      setInterests([...interests, id]);
    }
  };

  const validate = (): boolean => {
    const errors: Record<string, string> = {};

    if (!destination.trim()) {
      errors.destination = 'Please enter a travel destination.';
    } else if (destination.trim().length < 2) {
      errors.destination = 'Destination name must be at least 2 characters.';
    }

    if (!startDate) {
      errors.startDate = 'Start date is required.';
    } else if (startDate < today) {
      errors.startDate = 'Start date cannot be in the past.';
    }

    if (!endDate) {
      errors.endDate = 'End date is required.';
    } else if (endDate < startDate) {
      errors.endDate = 'End date cannot be earlier than start date.';
    } else if (tripDays > 14) {
      errors.endDate = 'Trip duration cannot exceed 14 days.';
    }

    const budgetCheck = parseAndValidateBudget(budget);
    if (!budgetCheck.isValid) {
      errors.budget = budgetCheck.error || 'Please enter a valid positive budget amount.';
    }

    if (groupSize < 1 || groupSize > 50) {
      errors.groupSize = 'Group size must be between 1 and 50 travelers.';
    }

    if (interests.length === 0) {
      errors.interests = 'Please select at least one interest.';
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    const budgetCheck = parseAndValidateBudget(budget);
    if (!budgetCheck.isValid || budgetCheck.value === undefined) return;

    onSubmit({
      destination: destination.trim(),
      start_date: startDate,
      end_date: endDate,
      budget: budgetCheck.value,
      currency,
      interests,
      travel_style: travelStyle,
      group_size: groupSize,
      special_preferences: specialPreferences.trim() || undefined,
    });
  };

  return (
    <div className="max-w-4xl mx-auto px-4 pb-16">
      <form
        onSubmit={handleSubmit}
        noValidate
        className="bg-white rounded-3xl p-6 sm:p-10 shadow-soft-lg border border-ivory-200"
      >
        <div className="border-b border-ivory-200 pb-6 mb-8">
          <h2 className="font-editorial text-2xl sm:text-3xl font-bold text-midnight-950">
            Design Your Trip
          </h2>
          <p className="text-midnight-600 text-sm mt-1">
            Fill in your trip details to generate a verified, schedule-clustered itinerary with transparent cost projections.
          </p>
        </div>

        <div className="space-y-8">
          {/* Destination Section */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-2">
              Where do you want to go? *
            </label>
            <div className="relative">
              <MapPin className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-midnight-400" />
              <input
                type="text"
                value={destination}
                onChange={(e) => {
                  setDestination(e.target.value);
                  if (fieldErrors.destination) setFieldErrors({ ...fieldErrors, destination: '' });
                }}
                placeholder="e.g. Jaipur, Rajasthan or Paris, France"
                className={`w-full pl-12 pr-4 py-3.5 rounded-2xl border text-sm sm:text-base font-medium transition-all ${
                  fieldErrors.destination
                    ? 'border-rose-400 bg-rose-50/30 text-rose-950 focus:ring-2 focus:ring-rose-500'
                    : 'border-ivory-300 bg-ivory-50/40 text-midnight-950 focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20'
                }`}
              />
            </div>
            {fieldErrors.destination && (
              <p className="flex items-center gap-1.5 text-xs text-rose-600 mt-2 font-medium">
                <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                {fieldErrors.destination}
              </p>
            )}

            {/* Quick Destination Pills */}
            <div className="flex flex-wrap items-center gap-1.5 mt-3">
              <span className="text-[11px] font-semibold text-midnight-400 mr-1 uppercase tracking-wider">
                Popular:
              </span>
              {POPULAR_DESTINATIONS.map((city) => (
                <button
                  key={city}
                  type="button"
                  onClick={() => {
                    setDestination(city);
                    if (fieldErrors.destination) setFieldErrors({ ...fieldErrors, destination: '' });
                  }}
                  className={`text-xs px-2.5 py-1 rounded-full border transition-colors ${
                    destination === city
                      ? 'bg-wanderteal-50 border-wanderteal-500 text-wanderteal-700 font-semibold'
                      : 'bg-ivory-100 border-ivory-200 text-midnight-700 hover:bg-ivory-200'
                  }`}
                >
                  {city.split(',')[0]}
                </button>
              ))}
            </div>
          </div>

          {/* Travel Dates & Duration */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-2">
                Travel Start Date *
              </label>
              <div className="relative">
                <Calendar className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-midnight-400" />
                <input
                  type="date"
                  min={today}
                  value={startDate}
                  onChange={(e) => {
                    setStartDate(e.target.value);
                    if (fieldErrors.startDate) setFieldErrors({ ...fieldErrors, startDate: '' });
                  }}
                  className="w-full pl-11 pr-4 py-3 rounded-2xl border border-ivory-300 bg-ivory-50/40 text-sm font-medium focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
                />
              </div>
              {fieldErrors.startDate && (
                <p className="flex items-center gap-1.5 text-xs text-rose-600 mt-1.5 font-medium">
                  <AlertCircle className="w-3.5 h-3.5" />
                  {fieldErrors.startDate}
                </p>
              )}
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-bold uppercase tracking-wider text-midnight-800">
                  Travel End Date *
                </label>
                {tripDays > 0 && (
                  <span className="inline-flex items-center gap-1 text-[11px] font-bold text-wanderteal-700 bg-wanderteal-50 px-2 py-0.5 rounded-md">
                    <Clock className="w-3 h-3" />
                    {tripDays} {tripDays === 1 ? 'Day' : 'Days'}
                  </span>
                )}
              </div>
              <div className="relative">
                <Calendar className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-midnight-400" />
                <input
                  type="date"
                  min={startDate || today}
                  value={endDate}
                  onChange={(e) => {
                    setEndDate(e.target.value);
                    if (fieldErrors.endDate) setFieldErrors({ ...fieldErrors, endDate: '' });
                  }}
                  className="w-full pl-11 pr-4 py-3 rounded-2xl border border-ivory-300 bg-ivory-50/40 text-sm font-medium focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
                />
              </div>
              {fieldErrors.endDate && (
                <p className="flex items-center gap-1.5 text-xs text-rose-600 mt-1.5 font-medium">
                  <AlertCircle className="w-3.5 h-3.5" />
                  {fieldErrors.endDate}
                </p>
              )}
            </div>
          </div>

          {/* Budget, Currency & Group Size */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="sm:col-span-2">
              <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-2">
                Total Trip Budget *
              </label>
              <div className="flex gap-2">
                <div className="w-28 shrink-0">
                  <select
                    value={currency}
                    onChange={(e) => setCurrency(e.target.value)}
                    className="w-full px-3 py-3 rounded-2xl border border-ivory-300 bg-ivory-50/40 text-sm font-semibold focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
                  >
                    {Object.keys(CURRENCY_SYMBOLS).map((code) => (
                      <option key={code} value={code}>
                        {code} ({CURRENCY_SYMBOLS[code]})
                      </option>
                    ))}
                  </select>
                </div>
                <div className="relative flex-1">
                  <Wallet className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-midnight-400" />
                  <input
                    type="text"
                    inputMode="decimal"
                    value={budget}
                    onChange={(e) => {
                      setBudget(e.target.value);
                      if (fieldErrors.budget) setFieldErrors({ ...fieldErrors, budget: '' });
                    }}
                    placeholder="e.g. 20000 or 20,000"
                    className="w-full pl-11 pr-4 py-3 rounded-2xl border border-ivory-300 bg-ivory-50/40 text-sm font-semibold focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
                  />
                </div>
              </div>
              {fieldErrors.budget && (
                <p className="flex items-center gap-1.5 text-xs text-rose-600 mt-1.5 font-medium">
                  <AlertCircle className="w-3.5 h-3.5" />
                  {fieldErrors.budget}
                </p>
              )}
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-2">
                Travelers *
              </label>
              <div className="relative">
                <Users className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-midnight-400" />
                <select
                  value={groupSize}
                  onChange={(e) => setGroupSize(parseInt(e.target.value, 10))}
                  className="w-full pl-11 pr-4 py-3 rounded-2xl border border-ivory-300 bg-ivory-50/40 text-sm font-semibold focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
                >
                  <option value={1}>1 Traveler (Solo)</option>
                  <option value={2}>2 Travelers (Couple)</option>
                  <option value={3}>3 Travelers (Small Group)</option>
                  <option value={4}>4 Travelers (Group)</option>
                  <option value={5}>5 Travelers</option>
                  <option value={6}>6+ Travelers (Family/Group)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Travel Style Radio Cards */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-3">
              Travel Style *
            </label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {TRAVEL_STYLES.map((style) => {
                const isSelected = travelStyle === style.id;
                return (
                  <button
                    key={style.id}
                    type="button"
                    onClick={() => setTravelStyle(style.id)}
                    className={`relative p-4 rounded-2xl border text-left transition-all ${
                      isSelected
                        ? 'border-wanderteal-600 bg-wanderteal-50/50 shadow-soft-sm ring-1 ring-wanderteal-600'
                        : 'border-ivory-200 bg-ivory-50/40 hover:bg-ivory-100/60'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="font-bold text-sm text-midnight-950">{style.title}</span>
                      <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-white border border-ivory-300 text-midnight-700">
                        {style.badge}
                      </span>
                    </div>
                    <p className="text-xs text-midnight-600 leading-relaxed mb-2">{style.desc}</p>
                    <div className="text-[11px] text-wanderteal-800 font-medium">
                      Stay: {style.accommodation}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Interests Chips */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="text-xs font-bold uppercase tracking-wider text-midnight-800">
                What interests you? (Select at least one) *
              </label>
              <span className="text-xs text-midnight-600 font-medium">
                {interests.length} selected
              </span>
            </div>
            <div className="flex flex-wrap gap-2">
              {AVAILABLE_INTERESTS.map((item) => {
                const isSelected = interests.includes(item.id);
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => toggleInterest(item.id)}
                    className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
                      isSelected
                        ? 'bg-midnight-900 text-ivory-50 shadow-soft-sm'
                        : 'bg-ivory-100 border border-ivory-200 text-midnight-800 hover:bg-ivory-200'
                    }`}
                  >
                    <span>{item.icon}</span>
                    <span>{item.label}</span>
                    {isSelected && <Check className="w-3 h-3 text-wanderteal-400 ml-0.5" />}
                  </button>
                );
              })}
            </div>
            {fieldErrors.interests && (
              <p className="flex items-center gap-1.5 text-xs text-rose-600 mt-2 font-medium">
                <AlertCircle className="w-3.5 h-3.5" />
                {fieldErrors.interests}
              </p>
            )}
          </div>

          {/* Optional Special Preferences */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-2">
              Optional Preferences or Special Requirements
            </label>
            <textarea
              rows={2}
              value={specialPreferences}
              onChange={(e) => setSpecialPreferences(e.target.value)}
              placeholder="e.g. Vegetarian dining only, slow morning pace, traveling with elderly parents, interested in architectural stepwells..."
              className="w-full px-4 py-3 rounded-2xl border border-ivory-300 bg-ivory-50/40 text-sm focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
            />
          </div>

          {/* Submit CTA */}
          <div className="pt-4 border-t border-ivory-200">
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-4 px-6 rounded-2xl bg-midnight-900 text-white font-bold text-base sm:text-lg flex items-center justify-center gap-3 hover:bg-midnight-800 active:scale-[0.99] transition-all disabled:opacity-60 disabled:cursor-not-allowed shadow-soft-md"
            >
              {isLoading ? (
                <>
                  <Compass className="w-5 h-5 animate-spin text-wanderteal-400" />
                  <span>Curating Your Itinerary...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5 text-wanderteal-400" />
                  <span>Create My Itinerary</span>
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>
            <p className="text-center text-[11px] text-midnight-600 mt-3">
              Includes geographic schedule clustering, realistic budget analysis, and editable day plans.
            </p>
          </div>
        </div>
      </form>

      {/* Educational Card: How WanderWise Works */}
      <div className="mt-8 p-6 rounded-2xl bg-ivory-100/70 border border-ivory-200 text-xs text-midnight-700 leading-relaxed">
        <h3 className="font-bold uppercase tracking-wider text-midnight-900 text-xs mb-2">
          How WanderWise Works
        </h3>
        <p className="mb-2">
          1. <strong>Geographic Verification:</strong> Validates your destination through geographic coordinates to verify authentic landmark locations and prevent fabricated attractions.
        </p>
        <p className="mb-2">
          2. <strong>Budget Realism Engine:</strong> Transparently itemizes lodging, meals, transit, and entry tickets. If the provided budget is mathematically insufficient for the destination, WanderWise highlights the budget gap with practical guidance.
        </p>
        <p>
          3. <strong>District Clustering:</strong> Schedules morning, afternoon, and evening sights in sequential neighborhood clusters to minimize transit time and avoid crisscrossing the city.
        </p>
      </div>
    </div>
  );
};
