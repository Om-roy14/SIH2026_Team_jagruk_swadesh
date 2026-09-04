import React from 'react';
import { motion } from 'framer-motion';

export default function Button({
  children,
  variant = 'primary', // 'primary' (dark forest pill), 'secondary' (translucent green pill), 'ghost'
  size = 'md', // 'sm', 'md', 'lg'
  icon: Icon,
  iconPosition = 'right',
  className = '',
  onClick,
  type = 'button',
  disabled = false,
  ...props
}) {
  const sizeClasses = {
    sm: 'px-4 py-2 text-xs font-semibold',
    md: 'px-5 py-2.5 text-sm font-semibold',
    lg: 'px-7 py-3.5 text-base font-semibold',
  };

  const variantClasses = {
    primary: 'btn-pill-primary',
    secondary: 'btn-pill-secondary',
    ghost: 'text-ivory-muted hover:text-white hover:bg-white/10 rounded-full transition-all',
  };

  return (
    <motion.button
      type={type}
      onClick={onClick}
      disabled={disabled}
      whileTap={{ scale: 0.97 }}
      className={`inline-flex items-center justify-center space-x-2 font-medium transition-all focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      {...props}
    >
      {Icon && iconPosition === 'left' && <Icon className="w-4 h-4 shrink-0" />}
      <span>{children}</span>
      {Icon && iconPosition === 'right' && <Icon className="w-4 h-4 shrink-0" />}
    </motion.button>
  );
}
