import React, { useState } from 'react';
import { X, Lock, Mail, ArrowRight, Database, CheckCircle2, AlertCircle } from 'lucide-react';
import { supabase, isSupabaseConfigured } from '../services/supabase';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (email: string) => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose, onSuccess }) => {
  if (!isOpen) return null;

  const [mode, setMode] = useState<'signin' | 'signup'>('signin');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isSupabaseConfigured || !supabase) {
      setErrorMsg('Supabase is not configured in this environment.');
      return;
    }

    setLoading(true);
    setErrorMsg('');
    setSuccessMsg('');

    try {
      if (mode === 'signup') {
        const { data, error } = await supabase.auth.signUp({
          email: email.trim(),
          password,
        });
        if (error) throw error;
        if (data.user) {
          setSuccessMsg('Account created successfully! You are now signed in.');
          onSuccess(email.trim());
          setTimeout(() => onClose(), 1500);
        }
      } else {
        const { data, error } = await supabase.auth.signInWithPassword({
          email: email.trim(),
          password,
        });
        if (error) throw error;
        if (data.user) {
          setSuccessMsg('Signed in successfully.');
          onSuccess(email.trim());
          setTimeout(() => onClose(), 1200);
        }
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Authentication failed. Please verify credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-midnight-950/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-elevated border border-ivory-200">
        <div className="flex items-center justify-between border-b border-ivory-200 pb-4 mb-5">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-midnight-900 text-wanderteal-400 flex items-center justify-center">
              <Lock className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-editorial text-xl font-bold text-midnight-950">
                {isSupabaseConfigured
                  ? mode === 'signin'
                    ? 'Sign In to WanderWise'
                    : 'Create WanderWise Account'
                  : 'Storage & Account Status'}
              </h3>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-midnight-500 hover:text-midnight-950 hover:bg-ivory-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {isSupabaseConfigured ? (
          <div>
            <p className="text-xs text-midnight-600 leading-relaxed mb-4">
              Sign in to automatically sync and access your customized travel itineraries across devices with Supabase Row-Level Security.
            </p>

            {errorMsg && (
              <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{errorMsg}</span>
              </div>
            )}

            {successMsg && (
              <div className="mb-4 p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 shrink-0" />
                <span>{successMsg}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-1.5">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-midnight-400" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="traveler@example.com"
                    className="w-full pl-10 pr-3.5 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-sm focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-midnight-800 mb-1.5">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-midnight-400" />
                  <input
                    type="password"
                    required
                    minLength={6}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full pl-10 pr-3.5 py-2.5 rounded-xl border border-ivory-300 bg-ivory-50/50 text-sm focus:border-wanderteal-600 focus:ring-2 focus:ring-wanderteal-500/20"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 rounded-xl bg-midnight-900 text-white text-xs font-bold flex items-center justify-center gap-2 hover:bg-midnight-800 transition-colors shadow-soft-sm disabled:opacity-50"
              >
                <span>{loading ? 'Authenticating...' : mode === 'signin' ? 'Sign In' : 'Create Account'}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>

            <div className="mt-4 pt-4 border-t border-ivory-200 text-center">
              <button
                type="button"
                onClick={() => setMode(mode === 'signin' ? 'signup' : 'signin')}
                className="text-xs text-wanderteal-700 hover:text-wanderteal-900 font-semibold"
              >
                {mode === 'signin'
                  ? "Don't have an account? Sign up here"
                  : 'Already have an account? Sign in'}
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="p-4 rounded-2xl bg-ivory-100/80 border border-ivory-200 text-xs text-midnight-700 leading-relaxed">
              <div className="flex items-center gap-2 font-bold text-midnight-950 mb-1.5">
                <Database className="w-4 h-4 text-amber-600" />
                <span>Supabase Database is Unconfigured</span>
              </div>
              <p className="mb-2">
                WanderWise is currently running in <strong>In-Memory Preview Mode</strong>. You can plan, view, edit, and save itineraries freely during your active browsing session.
              </p>
              <p>
                To enable persistent cloud storage across browser restarts, configure Supabase credentials in your <code>.env</code> file:
              </p>
              <pre className="mt-2 p-2.5 rounded-lg bg-midnight-950 text-wanderteal-300 text-[11px] font-mono overflow-x-auto">
{`VITE_SUPABASE_URL=https://xyz.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGci...`}
              </pre>
            </div>

            <button
              onClick={onClose}
              className="w-full py-3 px-4 rounded-xl bg-midnight-900 text-white text-xs font-bold flex items-center justify-center gap-2 hover:bg-midnight-800 transition-colors"
            >
              <span>Continue in Preview Mode</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
