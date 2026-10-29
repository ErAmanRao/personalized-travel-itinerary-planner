import React, { useState } from 'react';
import { X, Check } from 'lucide-react';
import { Activity } from '../types/travel';

interface EditActivityModalProps {
  activity: Activity | null;
  dayNumber: number;
  currency: string;
  isOpen: boolean;
  onClose: () => void;
  onSave: (dayNumber: number, updatedActivity: Activity) => void;
}

export const EditActivityModal: React.FC<EditActivityModalProps> = ({
  activity,
  dayNumber,
  currency,
  isOpen,
  onClose,
  onSave,
}) => {
  if (!isOpen || !activity) return null;

  const [title, setTitle] = useState(activity.title);
  const [timeSlot, setTimeSlot] = useState(activity.time_slot);
  const [category, setCategory] = useState(activity.category);
  const [cost, setCost] = useState(activity.estimated_cost.toString());
  const [description, setDescription] = useState(activity.description);
  const [transport, setTransport] = useState(activity.transport_guidance || '');

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    const updated: Activity = {
      ...activity,
      title: title.trim(),
      time_slot: timeSlot.trim(),
      category: category.trim(),
      estimated_cost: parseFloat(cost) || 0,
      description: description.trim(),
      transport_guidance: transport.trim() || undefined,
    };
    onSave(dayNumber, updated);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-midnight-950/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-elevated border border-ivory-200">
        <div className="flex items-center justify-between border-b border-ivory-200 pb-4 mb-5">
          <div>
            <span className="text-[10px] font-bold uppercase tracking-wider text-wanderteal-600">
              Day {dayNumber} Modification
            </span>
            <h3 className="font-editorial text-xl font-bold text-midnight-950">
              Edit Activity
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-midnight-500 hover:text-midnight-950 hover:bg-ivory-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSave} className="space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-1.5">
              Activity Title *
            </label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-sm font-semibold focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-1.5">
                Time Slot
              </label>
              <input
                type="text"
                value={timeSlot}
                onChange={(e) => setTimeSlot(e.target.value)}
                placeholder="Morning (09:30 - 12:00)"
                className="w-full px-3.5 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-xs font-medium focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-1.5">
                Category
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-xs font-semibold focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
              >
                <option value="Culture">Culture</option>
                <option value="History">History</option>
                <option value="Attraction">Attraction</option>
                <option value="Nature">Nature</option>
                <option value="Food">Food</option>
                <option value="Shopping">Shopping</option>
                <option value="Relaxation">Relaxation</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-1.5">
              Estimated Cost ({currency})
            </label>
            <input
              type="number"
              min="0"
              step="10"
              value={cost}
              onChange={(e) => setCost(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-sm font-medium focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-1.5">
              Description & Highlights
            </label>
            <textarea
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-xs leading-relaxed focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-1.5">
              Transit Guidance
            </label>
            <input
              type="text"
              value={transport}
              onChange={(e) => setTransport(e.target.value)}
              placeholder="e.g. 15 min metro or walking distance from old town"
              className="w-full px-3.5 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-xs focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
            />
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-ivory-200">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2.5 rounded-xl border border-ivory-300 text-xs font-bold text-midnight-700 hover:bg-ivory-100 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-5 py-2.5 rounded-xl bg-midnight-900 text-white text-xs font-bold flex items-center gap-1.5 hover:bg-midnight-800 transition-colors shadow-soft-sm"
            >
              <Check className="w-4 h-4 text-wanderteal-400" />
              Save Activity
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
