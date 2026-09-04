import React, { useEffect, useState } from 'react';

export default function CursorGlow() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Disable cursor glow on touch / mobile devices
    const isTouch = window.matchMedia('(pointer: coarse)').matches;
    if (isTouch) return;

    setMounted(true);

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let currentX = mouseX;
    let currentY = mouseY;
    let animationFrameId;

    const handleMouseMove = (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    };

    const animate = () => {
      // Smooth lerp (0.12 lerp speed)
      currentX += (mouseX - currentX) * 0.12;
      currentY += (mouseY - currentY) * 0.12;

      const cursorEl = document.getElementById('cursor-liquid-aura');
      if (cursorEl) {
        cursorEl.style.transform = `translate3d(${currentX - 160}px, ${currentY - 160}px, 0)`;
      }

      animationFrameId = requestAnimationFrame(animate);
    };

    window.addEventListener('mousemove', handleMouseMove, { passive: true });
    animationFrameId = requestAnimationFrame(animate);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  if (!mounted) return null;

  return (
    <div
      id="cursor-liquid-aura"
      className="fixed top-0 left-0 w-80 h-80 rounded-full pointer-events-none z-30 hidden md:block"
      style={{
        background: 'radial-gradient(circle, rgba(96, 150, 107, 0.14) 0%, rgba(45, 90, 55, 0.06) 50%, transparent 70%)',
        filter: 'blur(36px)',
        willChange: 'transform',
      }}
      aria-hidden="true"
    />
  );
}
