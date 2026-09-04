import React from 'react';

export default function Logo({ size = 'md', className = '', showText = true }) {
  const sizeClasses = {
    sm: 'h-8',
    md: 'h-10 sm:h-11',
    lg: 'h-14 sm:h-16',
  };

  return (
    <div className={`flex items-center space-x-3.5 group ${className}`}>
      {/* Official Jagruk Swadesh Logo Badge */}
      <div className="relative flex items-center justify-center p-1 rounded-xl bg-white border border-white/60 shadow-lg group-hover:scale-105 transition-transform duration-200 overflow-hidden shrink-0">
        <img
          src="/assets/logo.png"
          alt="Jagruk Swadesh Logo"
          className={`${sizeClasses[size]} w-auto object-contain shrink-0`}
          onError={(e) => {
            e.target.src = '/assets/logo-original.jpg';
          }}
        />
      </div>

      {showText && (
        <div className="flex flex-col text-left">
          <span className="text-base sm:text-lg font-extrabold tracking-tight text-white group-hover:text-amber-300 transition-colors leading-snug">
            Jagruk Swadesh
          </span>
          <span className="text-[11px] uppercase font-black text-amber-300 tracking-wider -mt-0.5">
            Smart Citizens. Stronger India.
          </span>
        </div>
      )}
    </div>
  );
}
