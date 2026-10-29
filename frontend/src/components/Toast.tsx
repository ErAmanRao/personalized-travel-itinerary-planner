import React from 'react';
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-react';

export interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'info';
  title: string;
  message?: string;
}

interface ToastProps {
  toasts: ToastMessage[];
  onDismiss: (id: string) => void;
}

export const Toast: React.FC<ToastProps> = ({ toasts, onDismiss }) => {
  if (toasts.length === 0) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-3 max-w-md w-full px-4 pointer-events-none">
      {toasts.map((t) => (
        <div
          key={t.id}
          className={`pointer-events-auto flex items-start gap-3 p-4 rounded-xl shadow-soft-lg border backdrop-blur-md transition-all duration-200 animate-slide-up ${
            t.type === 'success'
              ? 'bg-emerald-950/90 border-emerald-500/30 text-emerald-100'
              : t.type === 'error'
              ? 'bg-rose-950/90 border-rose-500/30 text-rose-100'
              : 'bg-midnight-900/90 border-midnight-700 text-ivory-100'
          }`}
        >
          {t.type === 'success' && <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />}
          {t.type === 'error' && <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />}
          {t.type === 'info' && <Info className="w-5 h-5 text-wanderteal-400 shrink-0 mt-0.5" />}

          <div className="flex-1 text-sm">
            <h4 className="font-semibold">{t.title}</h4>
            {t.message && <p className="opacity-90 mt-0.5 text-xs leading-relaxed">{t.message}</p>}
          </div>

          <button
            onClick={() => onDismiss(t.id)}
            className="text-ivory-300 hover:text-white p-1 rounded-lg transition-colors"
            aria-label="Dismiss notification"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      ))}
    </div>
  );
};
