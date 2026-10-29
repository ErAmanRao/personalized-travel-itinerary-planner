-- ====================================================================
-- WanderWise: Supabase Schema & Row-Level Security (RLS) Policies
-- ====================================================================
-- This schema stores user-owned personalized travel itineraries.
-- Run this script in the Supabase SQL Editor (Dashboard > SQL Editor > New Query).

-- 1. Create table for storing trips
CREATE TABLE IF NOT EXISTS public.trips (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    destination_name TEXT NOT NULL,
    country TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_days INTEGER NOT NULL CHECK (total_days >= 1),
    travel_style TEXT NOT NULL CHECK (travel_style IN ('budget', 'balanced', 'premium')),
    group_size INTEGER NOT NULL CHECK (group_size >= 1),
    currency TEXT NOT NULL DEFAULT 'INR',
    total_estimated_cost NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    image_url TEXT,
    itinerary_data JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- 2. Indexes for efficient lookup
CREATE INDEX IF NOT EXISTS idx_trips_user_id ON public.trips(user_id);
CREATE INDEX IF NOT EXISTS idx_trips_created_at ON public.trips(created_at DESC);

-- 3. Enable Row Level Security (RLS)
ALTER TABLE public.trips ENABLE ROW LEVEL SECURITY;

-- 4. RLS Policy: Users can select only their own saved trips
CREATE POLICY "Users can view their own trips"
    ON public.trips
    FOR SELECT
    USING (auth.uid() = user_id);

-- 5. RLS Policy: Users can insert their own trips
CREATE POLICY "Users can create their own trips"
    ON public.trips
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- 6. RLS Policy: Users can update their own trips
CREATE POLICY "Users can update their own trips"
    ON public.trips
    FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- 7. RLS Policy: Users can delete their own trips
CREATE POLICY "Users can delete their own trips"
    ON public.trips
    FOR DELETE
    USING (auth.uid() = user_id);

-- 8. Optional: Trigger to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_trips_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc'::text, now());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_trips_updated_at ON public.trips;
CREATE TRIGGER trigger_trips_updated_at
    BEFORE UPDATE ON public.trips
    FOR EACH ROW
    EXECUTE FUNCTION update_trips_updated_at();

-- Documentation Note:
-- If users are browsing as guests without logging in, itineraries are stored
-- in in-memory session preview on the backend, or cached locally.
-- When Supabase credentials are configured, the frontend/backend seamlessly
-- links trips to the signed-in user's auth.uid().
