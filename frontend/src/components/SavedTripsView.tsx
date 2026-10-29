import React, { useState } from 'react';
import {
  Bookmark,
  Calendar,
  Trash2,
  ArrowRight,
  Compass,
  MapPin,
  Clock,
  Database,
  Eye
} from 'lucide-react';
import { TripSummary } from '../types/travel';
import { formatDate } from '../utils/dates';
import { formatCurrency } from '../utils/currency';

interface SavedTripsViewProps {
  trips: TripSummary[];
  isSupabaseConnected: boolean;
  onSelectTrip: (tripId: string) => void;
  onDeleteTrip: (tripId: string) => void;
  onPlanNew: () => void;
}

export const SavedTripsView: React.FC<SavedTripsViewProps> = ({
  trips,
  isSupabaseConnected,
  onSelectTrip,
  onDeleteTrip,
  onPlanNew,
}) => {
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const handleDelete = (tripId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm('Are you sure you want to delete this saved itinerary?')) {
      setDeletingId(tripId);
      onDeleteTrip(tripId);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 pb-20">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-ivory-200 pb-6 mb-8">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-wanderteal-600 block mb-1">
            Personal Collection
          </span>
          <h2 className="font-editorial text-3xl sm:text-4xl font-bold text-midnight-950">
            Saved Itineraries
          </h2>
          <p className="text-xs sm:text-sm text-midnight-600 mt-1">
            {trips.length} {trips.length === 1 ? 'itinerary' : 'itineraries'} stored in{' '}
            {isSupabaseConnected ? 'Supabase cloud database' : 'session preview storage'}.
          </p>
        </div>

        <button
          onClick={onPlanNew}
          className="px-5 py-2.5 rounded-xl bg-midnight-900 text-white text-xs font-bold flex items-center gap-2 hover:bg-midnight-800 transition-colors shadow-soft-sm"
        >
          <Compass className="w-4 h-4 text-wanderteal-400" />
          <span>Plan New Trip</span>
        </button>
      </div>

      {/* Trips Grid or Empty State */}
      {trips.length === 0 ? (
        <div className="bg-white rounded-3xl p-12 text-center border border-ivory-200 shadow-soft-sm max-w-lg mx-auto my-12">
          <div className="w-14 h-14 rounded-2xl bg-ivory-100 text-midnight-400 mx-auto flex items-center justify-center mb-4">
            <Bookmark className="w-6 h-6" />
          </div>
          <h3 className="font-editorial text-xl font-bold text-midnight-950 mb-2">
            No saved itineraries yet
          </h3>
          <p className="text-xs text-midnight-600 leading-relaxed mb-6">
            Generate a personalized travel itinerary and click "Save Itinerary" to keep your curated plans accessible here.
          </p>
          <button
            onClick={onPlanNew}
            className="px-6 py-3 rounded-xl bg-midnight-900 text-white text-xs font-bold inline-flex items-center gap-2 hover:bg-midnight-800 transition-colors shadow-soft-sm"
          >
            <span>Start Planning Now</span>
            <ArrowRight className="w-4 h-4 text-wanderteal-400" />
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {trips.map((trip) => {
            const isDeleting = deletingId === trip.id;
            const fallbackImg =
              'https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80';

            return (
              <div
                key={trip.id}
                onClick={() => onSelectTrip(trip.id)}
                className="group cursor-pointer bg-white rounded-3xl overflow-hidden border border-ivory-200 shadow-soft-sm hover:shadow-soft-md hover:border-ivory-300 transition-all flex flex-col"
              >
                {/* Photo Header */}
                <div className="h-44 relative bg-midnight-900 overflow-hidden">
                  <img
                    src={trip.image_url || fallbackImg}
                    alt={trip.destination_name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 opacity-85"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = fallbackImg;
                    }}
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-midnight-950/80 via-transparent to-black/20" />

                  {/* Top Badges */}
                  <div className="absolute top-3 left-3 right-3 flex items-center justify-between">
                    <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full bg-white/90 backdrop-blur-sm text-midnight-900 shadow-soft-sm">
                      {trip.travel_style}
                    </span>
                    <button
                      onClick={(e) => handleDelete(trip.id, e)}
                      disabled={isDeleting}
                      title="Delete trip"
                      className="p-1.5 rounded-full bg-black/40 hover:bg-rose-600 text-white backdrop-blur-sm transition-colors"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  {/* Bottom Text Over Photo */}
                  <div className="absolute bottom-3 left-3 right-3">
                    <h3 className="font-editorial text-lg font-bold text-white leading-tight drop-shadow-sm">
                      {trip.destination_name}
                    </h3>
                  </div>
                </div>

                {/* Body Details */}
                <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
                  <div className="space-y-2 text-xs text-midnight-600">
                    <div className="flex items-center gap-1.5">
                      <Calendar className="w-3.5 h-3.5 text-midnight-400 shrink-0" />
                      <span>
                        {formatDate(trip.start_date)} – {formatDate(trip.end_date)}
                      </span>
                    </div>

                    <div className="flex items-center justify-between pt-1">
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-wanderteal-700 bg-wanderteal-50 px-2 py-0.5 rounded-md">
                        <Clock className="w-3 h-3" />
                        {trip.total_days} {trip.total_days === 1 ? 'Day' : 'Days'}
                      </span>
                      <span className="font-bold text-midnight-950 text-sm">
                        {formatCurrency(trip.total_estimated_cost, trip.currency)}
                      </span>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-ivory-200 flex items-center justify-between text-xs font-bold text-wanderteal-700 group-hover:text-wanderteal-800">
                    <span className="flex items-center gap-1">
                      <Eye className="w-3.5 h-3.5" />
                      View Full Itinerary
                    </span>
                    <ArrowRight className="w-3.5 h-3.5 transform group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
