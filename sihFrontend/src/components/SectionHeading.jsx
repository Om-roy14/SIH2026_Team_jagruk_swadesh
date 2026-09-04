import React from 'react';

export default function SectionHeading({
  tag,
  title,
  subtitle,
  center = true,
  className = ''
}) {
  return (
    <div className={`space-y-4 max-w-3xl ${center ? 'mx-auto text-center' : ''} ${className}`}>
      {tag && (
        <div className={`inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-forest-deep/90 border border-white/15 text-ivory-dim text-xs font-semibold uppercase tracking-wider ${center ? 'mx-auto' : ''}`}>
          <span className="text-emerald-400 font-bold">+</span>
          <span>{tag}</span>
        </div>
      )}
      {title && (
        <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white tracking-tight leading-tight">
          {title}
        </h2>
      )}
      {subtitle && (
        <div className="inline-block max-w-2xl">
          <p className="text-xs sm:text-sm text-ivory-muted leading-relaxed font-medium px-4 py-2 rounded-xl bg-forest-dark/90 backdrop-blur-md border border-white/12 shadow-md">
            {subtitle}
          </p>
        </div>
      )}
    </div>
  );
}
