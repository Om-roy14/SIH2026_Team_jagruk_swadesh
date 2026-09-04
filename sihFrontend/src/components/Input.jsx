import React from 'react';
import { Eye, EyeOff } from 'lucide-react';

export default function Input({
  label,
  type = 'text',
  name,
  value,
  onChange,
  placeholder,
  error,
  icon: Icon,
  required = false,
  className = '',
  // Password Show/Hide Toggle Props
  isPassword = false,
  showPassword = false,
  onTogglePassword,
  ...props
}) {
  const inputType = isPassword ? (showPassword ? 'text' : 'password') : type;

  return (
    <div className={`space-y-1.5 ${className}`}>
      {label && (
        <label htmlFor={name} className="block text-xs font-bold text-white uppercase tracking-wider text-shadow-sm">
          {label} {required && <span className="text-saffron">*</span>}
        </label>
      )}
      <div className="relative">
        {Icon && (
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-amber-300">
            <Icon className="w-4 h-4" />
          </div>
        )}
        <input
          type={inputType}
          id={name}
          name={name}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
          className={`liquid-input w-full ${Icon ? 'pl-10' : 'pl-4'} ${isPassword ? 'pr-11' : 'pr-4'} ${
            error ? 'border-red-400/80 focus:border-red-400' : ''
          }`}
          {...props}
        />

        {/* Eye Toggle Button for Password Fields */}
        {isPassword && onTogglePassword && (
          <button
            type="button"
            onClick={onTogglePassword}
            className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-amber-300/80 hover:text-amber-300 transition-colors focus:outline-none"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
            title={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? (
              <EyeOff className="w-4 h-4" />
            ) : (
              <Eye className="w-4 h-4" />
            )}
          </button>
        )}
      </div>
      {error && (
        <p className="text-xs text-red-400 font-bold pl-1">{error}</p>
      )}
    </div>
  );
}
