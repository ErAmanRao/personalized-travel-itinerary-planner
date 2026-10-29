import React from 'react';
import { Compass, Bookmark, User, Database, Sparkles, LogOut } from 'lucide-react';
import { User as SupabaseUser } from '@supabase/supabase-js';

interface NavbarProps {
  activeView: 'planner' | 'itinerary' | 'saved';
  onViewChange: (view: 'planner' | 'itinerary' | 'saved') => void;
  savedCount: number;
  hasActiveTrip: boolean;
  currentUser: SupabaseUser | null;
  isSupabaseConnected: boolean;
  onOpenAuth: () => void;
  onSignOut: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeView,
  onViewChange,
  savedCount,
  hasActiveTrip,
  currentUser,
  isSupabaseConnected,
  onOpenAuth,
  onSignOut,
}) => {
  return (
    <header className="sticky top-0 z-40 bg-ivory-50/90 backdrop-blur-md border-b border-ivory-200 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        
        {/* Brand Logo & Wordmark */}
        <button
          onClick={() => onViewChange('planner')}
          className="flex items-center gap-3 text-left focus:outline-none focus:ring-2 focus:ring-wanderteal-500 rounded-xl p-1"
        >
          <div className="w-10 h-10 rounded-xl bg-midnight-900 flex items-center justify-center text-wanderteal-400 shadow-soft-sm">
            <Compass className="w-6 h-6 animate-spin-slow" />
          </div>
          <div>
            <span className="font-editorial text-2xl font-bold tracking-tight text-midnight-950 flex items-center gap-1.5">
              WanderWise
            </span>
            <span className="text-[10px] font-semibold uppercase tracking-widest text-midnight-600 block -mt-1">
              Personalized Travel Planner
            </span>
          </div>
        </button>

        {/* Center Nav Links */}
        <nav className="hidden md:flex items-center gap-1 bg-ivory-100 p-1.5 rounded-full border border-ivory-200">
          <button
            onClick={() => onViewChange('planner')}
            className={`px-4 py-2 rounded-full text-xs font-semibold tracking-wide transition-all ${
              activeView === 'planner'
                ? 'bg-midnight-900 text-ivory-50 shadow-soft-sm'
                : 'text-midnight-700 hover:text-midnight-950 hover:bg-ivory-200/60'
            }`}
          >
            Plan Itinerary
          </button>

          {hasActiveTrip && (
            <button
              onClick={() => onViewChange('itinerary')}
              className={`px-4 py-2 rounded-full text-xs font-semibold tracking-wide transition-all flex items-center gap-1.5 ${
                activeView === 'itinerary'
                  ? 'bg-midnight-900 text-ivory-50 shadow-soft-sm'
                  : 'text-midnight-700 hover:text-midnight-950 hover:bg-ivory-200/60'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-wanderteal-500" />
              Active Trip
            </button>
          )}

          <button
            onClick={() => onViewChange('saved')}
            className={`px-4 py-2 rounded-full text-xs font-semibold tracking-wide transition-all flex items-center gap-1.5 ${
              activeView === 'saved'
                ? 'bg-midnight-900 text-ivory-50 shadow-soft-sm'
                : 'text-midnight-700 hover:text-midnight-950 hover:bg-ivory-200/60'
            }`}
          >
            <Bookmark className="w-3.5 h-3.5" />
            Saved Trips
            {savedCount > 0 && (
              <span className="ml-1 bg-wanderteal-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">
                {savedCount}
              </span>
            )}
          </button>
        </nav>

        {/* Right Actions: Storage Pill & Auth */}
        <div className="flex items-center gap-3">
          {/* Storage / Supabase Indicator Pill */}
          <div
            title={
              isSupabaseConnected
                ? 'Supabase database is connected for persistent cloud storage.'
                : 'Operating in preview mode (in-memory). Configure SUPABASE_URL in .env to permanently store trips.'
            }
            className={`hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-full text-[11px] font-medium border ${
              isSupabaseConnected
                ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                : 'bg-amber-50 text-amber-800 border-amber-200'
            }`}
          >
            <Database className="w-3 h-3" />
            <span className="w-1.5 h-1.5 rounded-full animate-pulse bg-current" />
            <span>{isSupabaseConnected ? 'Supabase Cloud' : 'Session Preview'}</span>
          </div>

          {/* User Auth Button */}
          {currentUser ? (
            <div className="flex items-center gap-2">
              <span className="text-xs font-medium text-midnight-700 hidden lg:inline truncate max-w-[140px]">
                {currentUser.email}
              </span>
              <button
                onClick={onSignOut}
                title="Sign Out"
                className="p-2 rounded-xl border border-ivory-200 bg-ivory-100 text-midnight-700 hover:text-rose-600 hover:bg-rose-50 transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <button
              onClick={onOpenAuth}
              className="flex items-center gap-1.5 text-xs font-semibold px-3.5 py-2 rounded-xl bg-midnight-900 text-ivory-50 hover:bg-midnight-800 transition-colors shadow-soft-sm"
            >
              <User className="w-3.5 h-3.5 text-wanderteal-400" />
              <span>{isSupabaseConnected ? 'Sign In' : 'Account'}</span>
            </button>
          )}
        </div>

      </div>

      {/* Mobile Nav Bar */}
      <div className="md:hidden flex items-center justify-around border-t border-ivory-200 bg-ivory-100/60 py-2 px-4">
        <button
          onClick={() => onViewChange('planner')}
          className={`text-xs font-semibold px-3 py-1.5 rounded-lg ${
            activeView === 'planner' ? 'bg-midnight-900 text-white' : 'text-midnight-700'
          }`}
        >
          Plan Trip
        </button>
        {hasActiveTrip && (
          <button
            onClick={() => onViewChange('itinerary')}
            className={`text-xs font-semibold px-3 py-1.5 rounded-lg ${
              activeView === 'itinerary' ? 'bg-midnight-900 text-white' : 'text-midnight-700'
            }`}
          >
            Active Trip
          </button>
        )}
        <button
          onClick={() => onViewChange('saved')}
          className={`text-xs font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1 ${
            activeView === 'saved' ? 'bg-midnight-900 text-white' : 'text-midnight-700'
          }`}
        >
          Saved ({savedCount})
        </button>
      </div>
    </header>
  );
};
