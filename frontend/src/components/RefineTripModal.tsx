import React, { useState } from 'react';
import { X, Sliders, Sparkles } from 'lucide-react';

interface RefineTripModalProps {
  isOpen: boolean;
  isLoading: boolean;
  onClose: () => void;
  onConfirm: (instruction: string) => void;
}

const QUICK_REFINEMENTS = [
  'Make all meals vegetarian or plant-based',
  'Relax the daily schedule with more free leisure time',
  'Focus more on photography viewpoints and sunset spots',
  'Include budget-friendly street food markets',
];

export const RefineTripModal: React.FC<RefineTripModalProps> = ({
  isOpen,
  isLoading,
  onClose,
  onConfirm,
}) => {
  if (!isOpen) return null;

  const [instruction, setInstruction] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!instruction.trim()) return;
    onConfirm(instruction.trim());
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-midnight-950/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-elevated border border-ivory-200">
        <div className="flex items-center justify-between border-b border-ivory-200 pb-4 mb-5">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-sunset-50 text-sunset-700 flex items-center justify-center">
              <Sliders className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[10px] font-bold uppercase tracking-wider text-sunset-600">
                Itinerary Adjustment
              </span>
              <h3 className="font-editorial text-xl font-bold text-midnight-950">
                Refine Itinerary
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
          Provide additional constraints or preferences to adapt dining choices, daily pacing, and focus areas across the entire trip.
        </p>

        {/* Quick Refinement Pills */}
        <div className="space-y-1.5 mb-4">
          <span className="text-[10px] font-bold uppercase tracking-wider text-midnight-500">
            Suggested Refinements:
          </span>
          <div className="flex flex-col gap-1.5">
            {QUICK_REFINEMENTS.map((q) => (
              <button
                key={q}
                type="button"
                onClick={() => setInstruction(q)}
                className="text-left text-xs p-2 rounded-xl bg-ivory-100 hover:bg-ivory-200 text-midnight-800 transition-colors border border-ivory-200"
              >
                + {q}
              </button>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-1.5">
              Your Refinement Instructions *
            </label>
            <textarea
              required
              rows={3}
              value={instruction}
              onChange={(e) => setInstruction(e.target.value)}
              placeholder="e.g. Ensure all dining suggestions are vegetarian-friendly and schedule a relaxed 2-hour tea break each afternoon..."
              className="w-full px-3.5 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-xs leading-relaxed focus:border-sunset-500 focus:ring-2 focus:ring-sunset-500/20"
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
              disabled={isLoading || !instruction.trim()}
              className="px-5 py-2.5 rounded-xl bg-midnight-900 text-white text-xs font-bold flex items-center gap-2 hover:bg-midnight-800 transition-colors shadow-soft-sm disabled:opacity-50"
            >
              <Sparkles className="w-3.5 h-3.5 text-sunset-400" />
              <span>{isLoading ? 'Applying...' : 'Apply Refinements'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
