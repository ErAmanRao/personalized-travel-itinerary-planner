import React, { useState } from 'react';
import { Camera, CameraOff, CheckCircle2, MapPin, ExternalLink } from 'lucide-react';
import { DestinationInfo } from '../types/travel';

interface DestinationPhotoCardProps {
  destination: DestinationInfo;
}

export const DestinationPhotoCard: React.FC<DestinationPhotoCardProps> = ({ destination }) => {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [hasError, setHasError] = useState<boolean>(false);

  const isAvailable = Boolean(
    destination.image_url &&
    destination.image_status !== 'unavailable' &&
    !hasError
  );

  return (
    <div className="w-full">
      {isAvailable ? (
        <div className="relative rounded-3xl overflow-hidden border border-white/20 shadow-soft-lg bg-midnight-950 aspect-[4/3] sm:aspect-[16/11] w-full group">
          {/* Subtle Skeleton Shimmer while loading */}
          {isLoading && (
            <div className="absolute inset-0 bg-midnight-900 animate-pulse flex flex-col items-center justify-center p-6 text-center">
              <Camera className="w-8 h-8 text-white/30 animate-bounce mb-2" />
              <span className="text-xs text-ivory-300 font-medium">Loading destination imagery...</span>
            </div>
          )}

          {/* Large Destination Photo */}
          <img
            src={destination.image_url!}
            alt={destination.resolved_name}
            onLoad={() => setIsLoading(false)}
            onError={() => {
              setIsLoading(false);
              setHasError(true);
            }}
            className={`w-full h-full object-cover transition-all duration-700 ease-out ${
              isLoading ? 'opacity-0 scale-95' : 'opacity-100 scale-100 group-hover:scale-105'
            }`}
          />

          {/* Top Destination Badge */}
          <div className="absolute top-3.5 left-3.5 flex items-center gap-1.5 px-3 py-1 rounded-full bg-midnight-950/80 backdrop-blur-md border border-white/20 text-white text-[11px] font-semibold shadow-soft-sm">
            <MapPin className="w-3.5 h-3.5 text-wanderteal-400" />
            <span className="truncate max-w-[180px]">{destination.resolved_name}</span>
          </div>

          {/* Verified Match Badge */}
          <div className="absolute top-3.5 right-3.5 px-2.5 py-1 rounded-full bg-emerald-600/90 backdrop-blur-md text-white text-[10px] font-bold uppercase tracking-wider flex items-center gap-1 shadow-soft-sm">
            <CheckCircle2 className="w-3 h-3 text-emerald-200" />
            <span>{destination.image_status === 'verified' ? 'Verified Match' : 'Destination Photo'}</span>
          </div>

          {/* Photographer Attribution Bar (Unsplash & License Compliance) */}
          <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-midnight-950/95 via-midnight-950/60 to-transparent p-3.5 pt-8 flex items-end justify-between text-[11px] text-ivory-200 backdrop-blur-[1px]">
            <div>
              {destination.photographer_name ? (
                <p className="leading-tight">
                  <span className="text-ivory-400 text-[10px] block">Photograph by</span>
                  {destination.photographer_url ? (
                    <a
                      href={destination.photographer_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-white font-semibold hover:text-wanderteal-300 underline underline-offset-2 transition-colors"
                    >
                      <span>{destination.photographer_name}</span>
                      <ExternalLink className="w-3 h-3 opacity-70" />
                    </a>
                  ) : (
                    <span className="text-white font-semibold">{destination.photographer_name}</span>
                  )}
                </p>
              ) : (
                <span className="text-ivory-300 font-medium">Verified Destination Photography</span>
              )}
            </div>

            <span className="text-[10px] uppercase font-bold tracking-wider text-wanderteal-400 bg-midnight-900/60 px-2 py-0.5 rounded-md border border-white/10">
              {destination.country}
            </span>
          </div>
        </div>
      ) : (
        /* Tasteful Designed Placeholder when photo is unavailable or API fails */
        <div className="relative rounded-3xl overflow-hidden border border-white/15 shadow-soft-md bg-gradient-to-br from-midnight-900 via-midnight-950 to-midnight-900 aspect-[4/3] sm:aspect-[16/11] w-full flex flex-col items-center justify-center p-6 text-center text-ivory-100">
          <div className="w-14 h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-3 text-ivory-400 shadow-inner">
            <CameraOff className="w-7 h-7 text-sunset-400" />
          </div>

          <h4 className="font-editorial text-lg sm:text-xl font-bold text-white mb-1.5 leading-snug">
            {destination.resolved_name}
          </h4>

          <span className="inline-block px-3 py-1 rounded-full bg-amber-500/20 border border-amber-400/30 text-amber-300 text-[10px] font-bold uppercase tracking-wider mb-2">
            Image Unavailable
          </span>

          <p className="text-xs text-ivory-300/80 max-w-xs leading-relaxed">
            No confirmed photograph found for this specific location. WanderWise shows only verified destination imagery and avoids generic placeholder photos.
          </p>

          <div className="mt-3 inline-flex items-center gap-1 text-[11px] text-wanderteal-400 font-medium">
            <MapPin className="w-3.5 h-3.5" />
            <span>Itinerary fully structured below</span>
          </div>
        </div>
      )}
    </div>
  );
};
