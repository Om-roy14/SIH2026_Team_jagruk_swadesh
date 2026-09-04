import React from 'react';
import { motion } from 'framer-motion';

export default function LiquidCard({
  children,
  className = '',
  hoverEffect = true,
  onClick,
  ...props
}) {
  return (
    <motion.div
      whileHover={hoverEffect ? { y: -3, scale: 1.004 } : undefined}
      transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
      onClick={onClick}
      className={`liquid-card p-6 sm:p-7 ${className} ${onClick ? 'cursor-pointer' : ''}`}
      {...props}
    >
      {children}
    </motion.div>
  );
}
