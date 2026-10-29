import React, { useState } from 'react';
import { X, RefreshCw, Sparkles } from 'lucide-react';

interface RegenerateDayModalProps {
  dayNumber: number;
  isOpen: boolean;
  isLoading: boolean;
  onClose: () => void;
  onConfirm: (dayNumber: number, focusNote?: string) => void;
}

export const RegenerateDayModal: React.FC<RegenerateDayModalProps> = ({
  dayNumber,
  isOpen,
  isLoading,
  onClose,
  onConfirm,
}) => {
  if (!isOpen) return null;

  const [focusNote, setFocusNote] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onConfirm(dayNumber, focusNote.trim() || undefined);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-midnight-950/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-elevated border border-ivory-200">
        <div className="flex items-center justify-between border-b border-ivory-200 pb-4 mb-5">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-wanderteal-50 text-wanderteal-700 flex items-center justify-center">
              <RefreshCw className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-bold uppercase tracking-wider text-wanderteal-600">
                Single Day Refresh
              </span>
              <h3 className="font-editorial text-xl font-bold text-midnight-950">
                Regenerate Day {dayNumber}
              </h3>
            </div>
          </div>
          <button
            onClick={onClose}
            disabled={isLoading}
            className="p-1.5 rounded-lg text-midnight-500 hover:text-midnight-950 hover:bg-ivory-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <p className="text-xs text-midnight-600 leading-relaxed mb-4">
          This will generate fresh morning, afternoon, and evening sights, meals, and route guidance for{' '}
          <strong>Day {dayNumber}</strong> only. All other days in your itinerary remain intact.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-1.5">
              Custom focus for this day (Optional)
            </label>
            <textarea
              rows={3}
              value={focusNote}
              onChange={(e) => setFocusNote(e.target.value)}
              placeholder="e.g. Focus on historic architecture and quiet sunset views, or prioritize food markets and cafes..."
              className="w-full px-3.5 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-xs leading-relaxed focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
            />
          </div>

          <div className="flex items-center justify-end gap-3 pt-3 border-t border-ivory-200">
            <button
              type="button"
              onClick={onClose}
              disabled={isLoading}
              className="px-4 py-2.5 rounded-xl border border-ivory-300 text-xs font-bold text-midnight-700 hover:bg-ivory-100 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="px-5 py-2.5 rounded-xl bg-midnight-900 text-white text-xs font-bold flex items-center gap-2 hover:bg-midnight-800 transition-colors shadow-soft-sm disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 text-wanderteal-400 ${isLoading ? 'animate-spin' : ''}`} />
              <span>{isLoading ? 'Regenerating...' : 'Regenerate Day'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
