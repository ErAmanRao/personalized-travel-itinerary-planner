import {
  TripRequest,
  Itinerary,
  DestinationInfo,
  TripSummary,
  BackendHealth
} from '../types/travel';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';

export class ApiError extends Error {
  status: number;
  details?: Array<{ field: string; message: string }>;

  constructor(message: string, status: number, details?: Array<{ field: string; message: string }>) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.details = details;
  }
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorMsg = `Server error (${res.status})`;
    let details: Array<{ field: string; message: string }> | undefined;
    try {
      const errorData = await res.json();
      errorMsg = errorData.message || errorData.detail || errorMsg;
      details = errorData.details;
    } catch {
      // JSON parse failed, use status text
      errorMsg = res.statusText || errorMsg;
    }
    throw new ApiError(errorMsg, res.status, details);
  }
  return res.json();
}

export const api = {
  async getHealth(): Promise<BackendHealth> {
    const res = await fetch(`${API_BASE}/health`);
    return handleResponse<BackendHealth>(res);
  },

  async verifyDestination(query: string): Promise<DestinationInfo> {
    const res = await fetch(`${API_BASE}/destinations/verify?query=${encodeURIComponent(query)}`);
    return handleResponse<DestinationInfo>(res);
  },

  async generateItinerary(req: TripRequest): Promise<Itinerary> {
    const res = await fetch(`${API_BASE}/itinerary/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req),
    });
    return handleResponse<Itinerary>(res);
  },

  async regenerateDay(itinerary: Itinerary, dayNumber: number, focusNote?: string): Promise<Itinerary> {
    const res = await fetch(`${API_BASE}/itinerary/regenerate-day`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        itinerary,
        day_number: dayNumber,
        focus_note: focusNote || null,
      }),
    });
    return handleResponse<Itinerary>(res);
  },

  async refineItinerary(itinerary: Itinerary, refinementInstruction: string): Promise<Itinerary> {
    const res = await fetch(`${API_BASE}/itinerary/refine`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        itinerary,
        refinement_instruction: refinementInstruction,
      }),
    });
    return handleResponse<Itinerary>(res);
  },

  async saveTrip(itinerary: Itinerary, userId?: string | null): Promise<{ success: boolean; storage_mode: string; message: string }> {
    const res = await fetch(`${API_BASE}/trips`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        itinerary,
        user_id: userId || null,
      }),
    });
    return handleResponse<{ success: boolean; storage_mode: string; message: string }>(res);
  },

  async getSavedTrips(userId?: string | null): Promise<TripSummary[]> {
    const url = userId ? `${API_BASE}/trips?user_id=${encodeURIComponent(userId)}` : `${API_BASE}/trips`;
    const res = await fetch(url);
    return handleResponse<TripSummary[]>(res);
  },

  async getTripById(tripId: string): Promise<Itinerary> {
    const res = await fetch(`${API_BASE}/trips/${tripId}`);
    return handleResponse<Itinerary>(res);
  },

  async deleteTrip(tripId: string): Promise<{ success: boolean; message: string }> {
    const res = await fetch(`${API_BASE}/trips/${tripId}`, {
      method: 'DELETE',
    });
    return handleResponse<{ success: boolean; message: string }>(res);
  },
};
