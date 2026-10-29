import React from 'react';
import { MapPin, Sparkles, Navigation2, CheckCircle2 } from 'lucide-react';

export const Hero: React.FC = () => {
  return (
    <section className="relative pt-12 pb-8 md:pt-16 md:pb-12 text-center max-w-4xl mx-auto px-4">
      {/* Editorial Pill */}
      <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-ivory-200 border border-ivory-300 text-midnight-800 text-xs font-semibold uppercase tracking-wider mb-6 shadow-soft-sm">
        <Sparkles className="w-3.5 h-3.5 text-wanderteal-600" />
        <span>Curated Travel Intelligence</span>
      </div>

      {/* Main Headline */}
      <h1 className="font-editorial text-4xl sm:text-5xl md:text-6xl font-bold tracking-tight text-midnight-950 leading-[1.15] mb-6">
        Curate your journey with <br className="hidden sm:inline" />
        <span className="italic font-normal text-wanderteal-600">rhythm</span>, <span className="text-sunset-600">taste</span>, and purpose.
      </h1>

      {/* Supporting Text */}
      <p className="text-base sm:text-lg text-midnight-700 max-w-2xl mx-auto leading-relaxed mb-8">
        WanderWise designs structured day-by-day travel itineraries with honest budget breakdown,
        geographic neighborhood clustering, and editable activities calibrated to your style.
      </p>

      {/* Three Editorial Highlights */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-left max-w-3xl mx-auto pt-2">
        <div className="flex items-start gap-3 p-3.5 rounded-xl bg-ivory-100/80 border border-ivory-200">
          <Navigation2 className="w-5 h-5 text-wanderteal-600 shrink-0 mt-0.5" />
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-midnight-900">Sensible Schedules</h4>
            <p className="text-xs text-midnight-600 mt-0.5">Clustered by district to prevent zigzagging transit.</p>
          </div>
        </div>

        <div className="flex items-start gap-3 p-3.5 rounded-xl bg-ivory-100/80 border border-ivory-200">
          <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-midnight-900">Budget Realism</h4>
            <p className="text-xs text-midnight-600 mt-0.5">Transparent breakdowns for stay, meals, transit, & tours.</p>
          </div>
        </div>

        <div className="flex items-start gap-3 p-3.5 rounded-xl bg-ivory-100/80 border border-ivory-200">
          <MapPin className="w-5 h-5 text-sunset-600 shrink-0 mt-0.5" />
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-midnight-900">Full Flexibility</h4>
            <p className="text-xs text-midnight-600 mt-0.5">Edit any activity, regenerate any day, or refine constraints.</p>
          </div>
        </div>
      </div>
    </section>
  );
};
