import React, { useState, useEffect } from 'react';
import { Compass, Sparkles } from 'lucide-react';

const TRAVEL_QUOTES = [
  "Clustering neighborhood sights to minimize travel time...",
  "Calibrating lodging and daily meal estimates...",
  "Verifying landmark schedules and local transit passes...",
  "Balancing cultural landmarks with authentic dining stops...",
  "Structuring sensible morning, afternoon, and golden-hour rhythms..."
];

export const LoadingSkeleton: React.FC = () => {
  const [quoteIdx, setQuoteIdx] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setQuoteIdx((prev) => (prev + 1) % TRAVEL_QUOTES.length);
    }, 2400);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="max-w-5xl mx-auto px-4 py-12 animate-pulse space-y-8">
      {/* Loading Banner Card */}
      <div className="bg-white rounded-3xl p-8 border border-ivory-200 shadow-soft-md text-center max-w-xl mx-auto">
        <div className="w-14 h-14 rounded-2xl bg-midnight-900 text-wanderteal-400 mx-auto flex items-center justify-center mb-4 shadow-soft-sm">
          <Compass className="w-7 h-7 animate-spin" />
        </div>
        <h3 className="font-editorial text-2xl font-bold text-midnight-950 mb-2">
          Curating Your Itinerary
        </h3>
        <p className="text-xs sm:text-sm text-midnight-600 font-medium h-6 transition-all duration-300">
          {TRAVEL_QUOTES[quoteIdx]}
        </p>
      </div>

      {/* Hero Banner Skeleton */}
      <div className="h-64 rounded-3xl bg-ivory-200/80 border border-ivory-300 relative overflow-hidden" />

      {/* Metrics Row Skeleton */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-24 rounded-2xl bg-white border border-ivory-200 p-4 space-y-2">
            <div className="h-3 w-16 bg-ivory-200 rounded" />
            <div className="h-6 w-24 bg-ivory-300 rounded" />
          </div>
        ))}
      </div>

      {/* Day Cards Skeleton */}
      <div className="space-y-4">
        <div className="h-10 w-64 bg-ivory-200 rounded-xl" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-44 rounded-2xl bg-white border border-ivory-200 p-5 space-y-3">
              <div className="h-4 w-24 bg-ivory-200 rounded" />
              <div className="h-5 w-40 bg-ivory-300 rounded" />
              <div className="h-12 w-full bg-ivory-100 rounded" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
