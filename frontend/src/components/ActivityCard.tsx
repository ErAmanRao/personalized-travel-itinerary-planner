import React from 'react';
import { Edit3, Navigation, Lightbulb, Tag } from 'lucide-react';
import { Activity } from '../types/travel';
import { formatCurrency } from '../utils/currency';

interface ActivityCardProps {
  activity: Activity;
  currency: string;
  onEdit: (activity: Activity) => void;
}

const CATEGORY_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  Culture: { bg: 'bg-amber-50', text: 'text-amber-800', border: 'border-amber-200' },
  History: { bg: 'bg-stone-100', text: 'text-stone-800', border: 'border-stone-200' },
  Attraction: { bg: 'bg-sky-50', text: 'text-sky-800', border: 'border-sky-200' },
  Nature: { bg: 'bg-emerald-50', text: 'text-emerald-800', border: 'border-emerald-200' },
  Food: { bg: 'bg-orange-50', text: 'text-orange-800', border: 'border-orange-200' },
  Shopping: { bg: 'bg-purple-50', text: 'text-purple-800', border: 'border-purple-200' },
  Relaxation: { bg: 'bg-teal-50', text: 'text-teal-800', border: 'border-teal-200' },
};

export const ActivityCard: React.FC<ActivityCardProps> = ({ activity, currency, onEdit }) => {
  const catStyle = CATEGORY_COLORS[activity.category] || {
    bg: 'bg-ivory-100',
    text: 'text-midnight-800',
    border: 'border-ivory-300',
  };

  const isFree = activity.estimated_cost === 0 || activity.cost_status === 'free';

  return (
    <div className="group relative bg-white rounded-2xl p-5 border border-ivory-200 shadow-soft-sm hover:shadow-soft-md transition-all">
      {/* Header: Time Slot, Category, Cost */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold uppercase tracking-wider text-midnight-800 bg-ivory-100 px-2.5 py-1 rounded-lg">
            {activity.time_slot}
          </span>
          <span
            className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border ${catStyle.bg} ${catStyle.text} ${catStyle.border}`}
          >
            {activity.category}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <span
            className={`text-xs font-bold px-2.5 py-1 rounded-lg border ${
              isFree
                ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                : 'bg-ivory-100 text-midnight-900 border-ivory-200'
            }`}
          >
            {isFree ? 'Free Admission' : formatCurrency(activity.estimated_cost, currency)}
          </span>

          <button
            onClick={() => onEdit(activity)}
            className="p-1.5 rounded-lg border border-transparent text-midnight-500 hover:text-midnight-950 hover:bg-ivory-100 hover:border-ivory-200 transition-colors"
            title="Edit activity"
            aria-label="Edit activity"
          >
            <Edit3 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Title */}
      <h4 className="font-editorial text-lg font-bold text-midnight-950 leading-snug mb-2">
        {activity.title}
      </h4>

      {/* Description */}
      <p className="text-xs sm:text-sm text-midnight-700 leading-relaxed mb-3">
        {activity.description}
      </p>

      {/* Transport Guidance */}
      {activity.transport_guidance && (
        <div className="flex items-center gap-2 text-xs text-midnight-600 bg-ivory-50/70 p-2.5 rounded-xl border border-ivory-200/80 mb-2">
          <Navigation className="w-3.5 h-3.5 text-wanderteal-600 shrink-0" />
          <span className="leading-snug">{activity.transport_guidance}</span>
        </div>
      )}

      {/* Tips */}
      {activity.tips && (
        <div className="flex items-start gap-2 text-xs text-amber-900 bg-amber-50/60 p-2.5 rounded-xl border border-amber-200/60">
          <Lightbulb className="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5" />
          <span className="leading-snug">{activity.tips}</span>
        </div>
      )}
    </div>
  );
};
