# WanderWise — Personalized Travel Itinerary Planner

**WanderWise** is a full-stack web application designed with a travel-editorial aesthetic that generates personalized, structured, day-by-day itineraries. It features geographic route clustering to eliminate crisscrossing transit, transparent budget itemization with realism checking, and full in-browser editability (activity editing, single-day regeneration, and itinerary refinement).

Built as an academic project adhering to strict software engineering standards, reliability, type-safety, and honest travel disclaimers.

---

## Architecture Overview

- **Frontend:** React 18 + Vite + TypeScript + Tailwind CSS
  - Palette: Midnight navy (`#0A1128`), warm ivory (`#FDFCF9`), tasteful teal (`#0D9488`), and restrained sunset orange (`#F97316`).
  - Typography: Playfair Display (editorial headings) & Plus Jakarta Sans (clean UI).
  - High-res photography with safe fallback placeholders that never display broken images.
- **Backend:** Python 3.13 + FastAPI REST API
  - Input validation through strict Pydantic v2 models.
  - Geographic destination verification via OpenStreetMap Nominatim and curated reference registry (rejects empty or gibberish input).
  - Budget Realism Engine: checks minimum baseline travel costs per destination and warns travelers of budget shortfalls with realistic recommendations.
- **AI & Curated Engine:**
  - Real configurable LLM support (Google Gemini 1.5 Flash / OpenAI GPT-4o-mini).
  - Zero-key Verified Curated Rule-Engine: if no API keys are provided or external APIs fail, WanderWise seamlessly generates verified, clustered itineraries with clear attribution labels.
- **Database & Authentication:**
  - Supabase integration with Row-Level Security (RLS) policies.
  - Automatic In-Memory Session Preview fallback when Supabase credentials are not configured, ensuring full feature usability without configuration barriers.

---

## Directory Structure

```
wanderwise/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   └── schemas.py              # Pydantic data schemas & validators
│   │   ├── routes/
│   │   │   ├── health.py               # Health & service readiness endpoint
│   │   │   ├── destinations.py         # Destination lookup & verification
│   │   │   ├── itinerary.py            # Generate, regenerate-day, refine endpoints
│   │   │   └── trips.py                # Save, list, get, delete trip endpoints
│   │   ├── services/
│   │   │   ├── destination_service.py        # Geocoding & registry verification
│   │   │   ├── destination_image_service.py  # Destination photo resolution & attribution
│   │   │   ├── budget_service.py             # Budget breakdown & realism analysis
│   │   │   ├── ai_service.py                 # Gemini/OpenAI API + Curated Engine
│   │   │   └── supabase_service.py           # Supabase persistence & in-memory preview
│   │   ├── config.py                   # Pydantic BaseSettings configuration
│   │   └── main.py                     # FastAPI application & CORS setup
│   ├── tests/
│   │   ├── test_validation.py          # Field validation & edge-case tests
│   │   ├── test_destination.py         # Known vs unverified destination tests
│   │   ├── test_budget.py              # Budget realism & math consistency tests
│   │   ├── test_itinerary.py           # Generation, day-regeneration & refinement tests
│   │   └── test_api_endpoints.py       # API route status & payload tests
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.tsx              # Brand header, nav links & storage pill
│   │   │   ├── Hero.tsx                # Magazine-style editorial hero
│   │   │   ├── TripPlannerForm.tsx     # Validated trip planning form
│   │   │   ├── ItineraryView.tsx       # Full results view & day tabs
│   │   │   ├── DestinationPhotoCard.tsx # Editorial hero photo card with attribution
│   │   │   ├── ActivityCard.tsx        # Activity card with time & edit CTA
│   │   │   ├── BudgetBreakdownCard.tsx # Category spend & per-person toggle
│   │   │   ├── EditActivityModal.tsx   # Activity edit dialog
│   │   │   ├── RegenerateDayModal.tsx  # Single day regeneration dialog
│   │   │   ├── RefineTripModal.tsx     # Global trip refinement dialog
│   │   │   ├── SavedTripsView.tsx      # Saved trips gallery
│   │   │   ├── AuthModal.tsx           # Supabase sign-in/up dialog
│   │   │   ├── Toast.tsx               # Notification toasts
│   │   │   └── LoadingSkeleton.tsx     # Editorial loading state
│   │   ├── services/
│   │   │   ├── api.ts                  # REST API client
│   │   │   └── supabase.ts             # Supabase client & auth state
│   │   ├── types/
│   │   │   └── travel.ts               # Complete TypeScript interfaces
│   │   ├── utils/
│   │   │   ├── currency.ts             # Currency formatting (INR ₹, USD, EUR, etc.)
│   │   │   └── dates.ts                # Date calculation & formatting
│   │   ├── App.tsx                     # Main application controller
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── supabase/
│   └── schema.sql                      # SQL table schema & RLS security policies
├── .env.example                        # Template environment variables
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites
- **Node.js** (v18 or higher) and `npm`
- **Python** (v3.10 or higher)

---

### Step 1: Backend Setup

1. Open a terminal and navigate to `backend/`:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   - **Windows:**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create your `.env` file (optional, template in `.env.example`):
   ```bash
   cp .env.example .env
   ```
   *(Note: WanderWise runs fully out-of-the-box using the built-in curated engine and in-memory preview storage even without any API keys).*

5. Run automated tests to verify your setup:
   ```bash
   pytest -v
   ```
   *(All 37 unit and integration tests should pass).*

6. Start the FastAPI backend server:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
   Interactive OpenAPI documentation is live at `http://127.0.0.1:8000/docs`.

---

### Step 2: Frontend Setup

1. Open a second terminal and navigate to `frontend/`:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. (Optional) Create `frontend/.env`:
   ```bash
   cp .env.example .env
   ```
   Default `VITE_API_BASE_URL` is configured to `http://127.0.0.1:8000/api` through Vite's dev proxy.

4. Verify the TypeScript production build:
   ```bash
   npm run build
   ```

5. Start the development server:
   ```bash
   npm run dev
   ```
   Open `http://localhost:5173` in your browser.

---

## Supabase Database Setup (Optional)

If you wish to enable permanent cross-device cloud persistence with user logins:

1. Create a free project at [supabase.com](https://supabase.com).
2. Go to the **SQL Editor** in your Supabase dashboard and run the script in `supabase/schema.sql`.
   - This creates the `trips` table with Row-Level Security (RLS) policies guaranteeing users can only read, update, and delete their own saved trips.
3. In `backend/.env`, set:
   ```env
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_ANON_KEY=your_supabase_anon_key
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
   ```
4. In `frontend/.env`, set:
   ```env
   VITE_SUPABASE_URL=https://your-project-id.supabase.co
   VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```
*(Note: Never expose the `SERVICE_ROLE_KEY` in frontend `.env`).*

If Supabase is not configured, WanderWise displays an unobtrusive "Session Preview" pill and stores saved itineraries in session memory so users can still explore all features without signing up.

---

## AI Generation Setup (Optional)

To enable live generative LLM responses:
1. Obtain a free Google Gemini API key from [Google AI Studio](https://aistudio.google.com).
2. Set in `backend/.env`:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   GEMINI_MODEL=gemini-1.5-flash
   ```
Alternatively, configure OpenAI:
```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
```
When keys are omitted, the application clearly labels itineraries as created by the **WanderWise Curated Rules Engine**, adhering to strict academic truthfulness.

---

## Simplest Deployment Guide

### Deploying Frontend (Vercel / Netlify)
1. Push repository to GitHub.
2. Link the repository on [Vercel](https://vercel.com) or [Netlify](https://netlify.com).
3. Set **Root Directory** to `frontend`.
4. Build command: `npm run build`, Output directory: `dist`.
5. Add Environment Variable:
   - `VITE_API_BASE_URL`: your deployed backend API URL (e.g. `https://wanderwise-api.onrender.com/api`).

### Deploying Backend (Render / Railway)
1. Create a new Web Service on [Render](https://render.com) from your GitHub repo.
2. Set **Root Directory** to `backend`.
3. Set **Build Command** to: `pip install -r requirements.txt`.
4. Set **Start Command** to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
5. Add Environment Variable:
   - `CORS_ORIGINS`: your frontend domain (e.g. `https://wanderwise.vercel.app`).

---

## License & Academic Disclaimer

This project is built for academic purposes. Travel recommendations, schedules, and cost estimates are designed for exploratory planning and must be independently verified by travelers before booking.
