import React, { useState, useEffect } from 'react';
import { User as SupabaseUser } from '@supabase/supabase-js';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { TripPlannerForm } from './components/TripPlannerForm';
import { ItineraryView } from './components/ItineraryView';
import { SavedTripsView } from './components/SavedTripsView';
import { LoadingSkeleton } from './components/LoadingSkeleton';
import { AuthModal } from './components/AuthModal';
import { Toast, ToastMessage } from './components/Toast';
import { api, ApiError } from './services/api';
import { supabase, isSupabaseConfigured, subscribeToAuthChanges } from './services/supabase';
import { TripRequest, Itinerary, TripSummary, Activity, BackendHealth } from './types/travel';

export function App() {
  const [activeView, setActiveView] = useState<'planner' | 'itinerary' | 'saved'>('planner');
  const [itinerary, setItinerary] = useState<Itinerary | null>(null);
  const [savedTrips, setSavedTrips] = useState<TripSummary[]>([]);
  const [backendHealth, setBackendHealth] = useState<BackendHealth | null>(null);

  // Loading states
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isRegenerating, setIsRegenerating] = useState<boolean>(false);
  const [isRefining, setIsRefining] = useState<boolean>(false);
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [isSaved, setIsSaved] = useState<boolean>(false);

  // Auth states
  const [currentUser, setCurrentUser] = useState<SupabaseUser | null>(null);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState<boolean>(false);

  // Toast notifications
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const addToast = (type: 'success' | 'error' | 'info', title: string, message?: string) => {
    const id = Date.now().toString();
    setToasts((prev) => [...prev, { id, type, title, message }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 5000);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  // Initial load: Fetch health & saved trips, listen to auth
  useEffect(() => {
    // 1. Health check
    api
      .getHealth()
      .then((h) => setBackendHealth(h))
      .catch((err) => console.warn('Could not fetch backend health:', err));

    // 2. Load saved trips
    loadSavedTrips();

    // 3. Supabase Auth listener
    const subscription = subscribeToAuthChanges((user) => {
      setCurrentUser(user);
      loadSavedTrips(user?.id);
    });

    return () => {
      subscription.unsubscribe();
    };
  }, []);

  const loadSavedTrips = async (userId?: string) => {
    try {
      const trips = await api.getSavedTrips(userId);
      setSavedTrips(trips);
    } catch (err) {
      console.warn('Failed to load saved trips:', err);
    }
  };

  // 1. Create Itinerary Handler
  const handleCreateItinerary = async (req: TripRequest) => {
    setIsLoading(true);
    setActiveView('itinerary');
    setIsSaved(false);

    try {
      const result = await api.generateItinerary(req);
      setItinerary(result);
      addToast(
        'success',
        'Itinerary Curated',
        `Structured ${result.total_days}-day plan created for ${result.destination.resolved_name}.`
      );
    } catch (err: any) {
      console.error('Itinerary generation error:', err);
      setActiveView('planner');
      const msg = err instanceof ApiError ? err.message : 'Unable to generate itinerary. Please verify inputs.';
      addToast('error', 'Generation Error', msg);
    } finally {
      setIsLoading(false);
    }
  };

  // 2. Update Single Activity Handler
  const handleUpdateActivity = (dayNumber: number, updatedActivity: Activity) => {
    if (!itinerary) return;

    const newDays = itinerary.days.map((d) => {
      if (d.day_number === dayNumber) {
        const updatedActivities = d.activities.map((a) => (a.id === updatedActivity.id ? updatedActivity : a));
        const actCost = updatedActivities.reduce((sum, a) => sum + (Number(a.estimated_cost) || 0), 0);
        const mealCost = d.meals.reduce((sum, m) => sum + (Number(m.estimated_cost) || 0), 0);
        const stayCost = Number(d.accommodation.estimated_nightly_cost) || 0;
        const transCost = Number(d.daily_transport_cost) || 0;
        const newDailyCost = Math.round((actCost + mealCost + stayCost + transCost) * 100) / 100;
        return {
          ...d,
          activities: updatedActivities,
          estimated_daily_cost: newDailyCost,
        };
      }
      return d;
    });

    // Rebuild budget breakdown with exact sum of all components
    const actTotal = Math.round(newDays.reduce((sum, d) => sum + d.activities.reduce((s, a) => s + (Number(a.estimated_cost) || 0), 0), 0) * 100) / 100;
    const foodTotal = Math.round(newDays.reduce((sum, d) => sum + d.meals.reduce((s, m) => s + (Number(m.estimated_cost) || 0), 0), 0) * 100) / 100;
    const stayTotal = Math.round(newDays.reduce((sum, d) => sum + (Number(d.accommodation.estimated_nightly_cost) || 0), 0) * 100) / 100;
    const transTotal = Math.round(newDays.reduce((sum, d) => sum + (Number(d.daily_transport_cost) || 0), 0) * 100) / 100;

    const newTotalCost = Math.round((actTotal + foodTotal + stayTotal + transTotal) * 100) / 100;
    const newPerPerson = Math.round((newTotalCost / itinerary.group_size) * 100) / 100;

    const newStatus =
      newTotalCost > itinerary.budget_breakdown.user_budget
        ? 'exceeds_budget'
        : !itinerary.budget_breakdown.is_realistic
        ? 'budget_alert'
        : itinerary.budget_breakdown.recommended_minimum_budget && itinerary.budget_breakdown.user_budget < itinerary.budget_breakdown.recommended_minimum_budget
        ? 'tight_budget'
        : 'within_budget';

    setItinerary({
      ...itinerary,
      days: newDays,
      budget_breakdown: {
        ...itinerary.budget_breakdown,
        activities_cost: actTotal,
        food_cost: foodTotal,
        accommodation_cost: stayTotal,
        local_transport_cost: transTotal,
        total_estimated_cost: newTotalCost,
        cost_per_person: newPerPerson,
        budget_status: newStatus,
      },
    });
    setIsSaved(false);
    addToast('success', 'Activity Updated', `Saved changes to "${updatedActivity.title}".`);
  };

  // 3. Regenerate Single Day Handler
  const handleRegenerateDay = async (dayNumber: number, focusNote?: string) => {
    if (!itinerary) return;
    setIsRegenerating(true);

    try {
      const updated = await api.regenerateDay(itinerary, dayNumber, focusNote);
      setItinerary(updated);
      setIsSaved(false);
      addToast(
        'success',
        `Day ${dayNumber} Regenerated`,
        focusNote ? `Updated with focus on: "${focusNote}"` : `New activities generated for Day ${dayNumber}.`
      );
    } catch (err: any) {
      console.error('Day regeneration error:', err);
      addToast('error', 'Regeneration Failed', err.message || 'Please retry.');
    } finally {
      setIsRegenerating(false);
    }
  };

  // 4. Refine Itinerary Handler
  const handleRefineTrip = async (instruction: string) => {
    if (!itinerary) return;
    setIsRefining(true);

    try {
      const refined = await api.refineItinerary(itinerary, instruction);
      setItinerary(refined);
      setIsSaved(false);
      addToast('success', 'Itinerary Refined', `Adapted to your instruction: "${instruction}"`);
    } catch (err: any) {
      console.error('Trip refinement error:', err);
      addToast('error', 'Refinement Failed', err.message || 'Please retry.');
    } finally {
      setIsRefining(false);
    }
  };

  // 5. Save Trip Handler
  const handleSaveTrip = async () => {
    if (!itinerary) return;
    setIsSaving(true);

    try {
      const result = await api.saveTrip(itinerary, currentUser?.id);
      setIsSaved(true);
      await loadSavedTrips(currentUser?.id);

      if (result.storage_mode === 'supabase_database') {
        addToast('success', 'Saved to Supabase', 'Itinerary is permanently stored in your Supabase account.');
      } else {
        addToast(
          'info',
          'Saved in Preview Mode',
          'Itinerary is saved for this active session. (Configure Supabase in .env for cross-session database sync).'
        );
      }
    } catch (err: any) {
      console.error('Save error:', err);
      addToast('error', 'Save Failed', err.message || 'Could not save itinerary.');
    } finally {
      setIsSaving(false);
    }
  };

  // 6. Select Saved Trip Handler
  const handleSelectSavedTrip = async (tripId: string) => {
    try {
      const trip = await api.getTripById(tripId);
      setItinerary(trip);
      setIsSaved(true);
      setActiveView('itinerary');
      addToast('info', 'Itinerary Loaded', `Displaying ${trip.title}`);
    } catch (err: any) {
      console.error('Error loading trip:', err);
      addToast('error', 'Load Error', 'Could not retrieve trip details.');
    }
  };

  // 7. Delete Saved Trip Handler
  const handleDeleteTrip = async (tripId: string) => {
    try {
      await api.deleteTrip(tripId);
      setSavedTrips((prev) => prev.filter((t) => t.id !== tripId));
      if (itinerary?.id === tripId) {
        setIsSaved(false);
      }
      addToast('info', 'Itinerary Deleted', 'The trip was removed from your saved list.');
    } catch (err: any) {
      console.error('Delete error:', err);
      addToast('error', 'Delete Failed', 'Could not delete trip.');
    }
  };

  const handleSignOut = async () => {
    if (supabase) {
      await supabase.auth.signOut();
      setCurrentUser(null);
      addToast('info', 'Signed Out', 'You have been signed out.');
    }
  };

  return (
    <div className="min-h-screen bg-ivory-50 flex flex-col text-midnight-950 font-sans selection:bg-wanderteal-100 selection:text-wanderteal-800">
      {/* Sticky Navigation Bar */}
      <Navbar
        activeView={activeView}
        onViewChange={setActiveView}
        savedCount={savedTrips.length}
        hasActiveTrip={Boolean(itinerary)}
        currentUser={currentUser}
        isSupabaseConnected={Boolean(backendHealth?.database.configured || isSupabaseConfigured)}
        onOpenAuth={() => setIsAuthModalOpen(true)}
        onSignOut={handleSignOut}
      />

      {/* Main Content Area */}
      <main className="flex-1">
        {/* VIEW 1: PLANNER (Home) */}
        {activeView === 'planner' && (
          <div>
            <Hero />
            <TripPlannerForm onSubmit={handleCreateItinerary} isLoading={isLoading} />
          </div>
        )}

        {/* VIEW 2: ITINERARY RESULTS */}
        {activeView === 'itinerary' && (
          <div>
            {isLoading ? (
              <LoadingSkeleton />
            ) : itinerary ? (
              <ItineraryView
                itinerary={itinerary}
                onUpdateActivity={handleUpdateActivity}
                onRegenerateDay={handleRegenerateDay}
                onRefineTrip={handleRefineTrip}
                onSaveTrip={handleSaveTrip}
                onPlanNew={() => setActiveView('planner')}
                isSaving={isSaving}
                isRegenerating={isRegenerating}
                isRefining={isRefining}
                isSaved={isSaved}
              />
            ) : (
              <div className="text-center py-24">
                <p className="text-sm text-midnight-600 mb-4">No active itinerary selected.</p>
                <button
                  onClick={() => setActiveView('planner')}
                  className="px-6 py-3 rounded-xl bg-midnight-900 text-white text-xs font-bold"
                >
                  Plan a Trip Now
                </button>
              </div>
            )}
          </div>
        )}

        {/* VIEW 3: SAVED TRIPS */}
        {activeView === 'saved' && (
          <SavedTripsView
            trips={savedTrips}
            isSupabaseConnected={Boolean(backendHealth?.database.configured || isSupabaseConfigured)}
            onSelectTrip={handleSelectSavedTrip}
            onDeleteTrip={handleDeleteTrip}
            onPlanNew={() => setActiveView('planner')}
          />
        )}
      </main>

      {/* Editorial Footer */}
      <footer className="border-t border-ivory-200 bg-ivory-100/70 py-10 px-4 mt-auto">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-midnight-600">
          <div className="flex items-center gap-2">
            <span className="font-editorial font-bold text-sm text-midnight-950">WanderWise</span>
            <span>— Personalized Travel Itinerary Planner</span>
          </div>

          <div className="text-center sm:text-right text-[11px] text-midnight-500 space-y-0.5">
            <p>Academic Project — Correctness, Reliability & Editorial UI/UX.</p>
            <p>Recommendations and cost breakdowns are planning estimates. Verify schedules and bookings prior to travel.</p>
          </div>
        </div>
      </footer>

      {/* Global Modals & Toast Stack */}
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onSuccess={(email) => {
          addToast('success', 'Signed In', `Welcome back, ${email}`);
        }}
      />

      <Toast toasts={toasts} onDismiss={removeToast} />
    </div>
  );
}

export default App;
