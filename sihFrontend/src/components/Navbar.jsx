import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X, ArrowUpRight, LogOut, UserCheck } from 'lucide-react';
import Button from './Button';
import Logo from './Logo';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const isChatbotPage = location.pathname === '/chatbot';

  const navLinks = isChatbotPage
    ? []
    : [
        { name: 'Home', path: '/' },
        { name: 'Explore', path: '/explore' },
        { name: 'About', path: '/about' },
      ];

  const isActive = (path) => location.pathname === path;

  return (
    <header className={`fixed top-0 left-0 right-0 z-40 transition-all duration-300 ${scrolled ? 'py-3' : 'py-5'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Floating Capsule Navbar Matching Reference */}
        <nav className={`liquid-nav-capsule px-5 sm:px-7 py-3 flex items-center justify-between transition-all duration-300 ${scrolled ? 'liquid-nav-capsule-scrolled' : ''}`}>
          
          {/* LEFT: Logo with Green Dot Indicator (Reference Inspired) */}
          <Link to="/" className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse shadow-sm" />
            <Logo size="md" />
          </Link>

          {/* CENTER / RIGHT: Navigation Links */}
          <div className="hidden md:flex items-center space-x-1 lg:space-x-2">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`relative px-4 py-1.5 text-sm font-medium rounded-full transition-all duration-200 ${
                  isActive(link.path)
                    ? 'text-white font-semibold'
                    : 'text-ivory-muted hover:text-white hover:bg-white/5'
                }`}
              >
                {isActive(link.path) && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute inset-0 bg-white/10 border border-white/15 rounded-full"
                    transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                  />
                )}
                <span className="relative z-10">{link.name}</span>
              </Link>
            ))}
          </div>

          {/* RIGHT: Login / Get Started / Authenticated Profile (ASK AI BUTTON REMOVED ENTIRELY) */}
          <div className="hidden md:flex items-center space-x-3">
            {isAuthenticated ? (
              <>
                <div className="flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-forest-deep/90 border border-white/15 text-xs font-semibold text-ivory-warm">
                  <UserCheck className="w-3.5 h-3.5 text-emerald-400" />
                  <span>{user?.name || 'Authenticated'}</span>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleLogout}
                  icon={LogOut}
                  title="Logout"
                >
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="ghost" size="sm">
                    Login
                  </Button>
                </Link>
                <Link to="/signup">
                  <Button variant="secondary" size="sm">
                    Get Started
                  </Button>
                </Link>
              </>
            )}
          </div>

          {/* Mobile Hamburger Toggle */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-full text-ivory-muted hover:text-white bg-white/5 border border-white/10 transition-colors"
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>

        </nav>
      </div>

      {/* Mobile Dropdown Navigation Drawer */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="md:hidden px-4 pt-2 pb-4"
          >
            <div className="liquid-glass-panel p-5 space-y-4 border-white/15">
              <div className="flex flex-col space-y-2">
                {navLinks.map((link) => (
                  <Link
                    key={link.path}
                    to={link.path}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`px-4 py-3 rounded-xl text-sm font-semibold transition-colors flex items-center justify-between ${
                      isActive(link.path)
                        ? 'bg-white/10 border border-white/15 text-white'
                        : 'text-ivory-muted hover:text-white hover:bg-white/5'
                    }`}
                  >
                    <span>{link.name}</span>
                    <ArrowUpRight className="w-4 h-4 opacity-70" />
                  </Link>
                ))}
              </div>

              <div className="pt-3 border-t border-white/10 grid grid-cols-2 gap-3">
                {isAuthenticated ? (
                  <Button variant="ghost" size="sm" onClick={() => { handleLogout(); setMobileMenuOpen(false); }} className="w-full col-span-2">
                    Logout ({user?.name || 'User'})
                  </Button>
                ) : (
                  <>
                    <Link to="/login" onClick={() => setMobileMenuOpen(false)}>
                      <Button variant="ghost" size="sm" className="w-full">
                        Login
                      </Button>
                    </Link>
                    <Link to="/signup" onClick={() => setMobileMenuOpen(false)}>
                      <Button variant="secondary" size="sm" className="w-full">
                        Get Started
                      </Button>
                    </Link>
                  </>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
