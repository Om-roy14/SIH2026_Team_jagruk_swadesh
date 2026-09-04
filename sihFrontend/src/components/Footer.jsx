import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, ArrowUpRight } from 'lucide-react';
import Logo from './Logo';

export default function Footer({ onOpenChatbotModal }) {
  return (
    <footer className="relative mt-24 border-t border-white/10 bg-forest-dark/95 backdrop-blur-xl text-ivory-muted text-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 lg:gap-12 pb-12 border-b border-white/10">
          
          {/* Brand Info with Official Logo */}
          <div className="lg:col-span-2 space-y-4">
            <Link to="/" className="inline-block">
              <Logo size="lg" />
            </Link>
            
            <p className="text-xs sm:text-sm text-ivory-dim leading-relaxed max-w-sm font-normal">
              Making BIS-related information easier to discover and understand. An intelligent platform empowering industries, MSMEs, startups, and Indian consumers.
            </p>

            <button
              onClick={onOpenChatbotModal}
              className="inline-flex items-center space-x-2 px-4 py-2 rounded-full bg-forest-olive/80 border border-white/15 text-white text-xs font-semibold hover:bg-forest-sage/60 transition-all shadow-sm"
            >
              <Sparkles className="w-3.5 h-3.5 text-emerald-300" />
              <span>Jagruk Swadesh AI Chatbot</span>
              <ArrowUpRight className="w-3.5 h-3.5 opacity-70" />
            </button>
          </div>

          {/* Navigation Links */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-white uppercase tracking-wider">Navigation</h4>
            <ul className="space-y-2 text-xs font-medium text-ivory-dim">
              <li>
                <Link to="/" className="hover:text-white transition-colors">Home</Link>
              </li>
              <li>
                <Link to="/explore" className="hover:text-white transition-colors">Explore Services</Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-white transition-colors">About Us</Link>
              </li>
            </ul>
          </div>

          {/* Services Links */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-white uppercase tracking-wider">BIS Services</h4>
            <ul className="space-y-2 text-xs font-medium text-ivory-dim">
              <li>
                <Link to="/explore" className="hover:text-white transition-colors">Indian Standards</Link>
              </li>
              <li>
                <Link to="/explore" className="hover:text-white transition-colors">Certification</Link>
              </li>
              <li>
                <Link to="/explore" className="hover:text-white transition-colors">Testing & Labs</Link>
              </li>
              <li>
                <Link to="/explore" className="hover:text-white transition-colors">Consumer Guidance</Link>
              </li>
            </ul>
          </div>

          {/* Account & Legal Links */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-white uppercase tracking-wider">Account & Legal</h4>
            <ul className="space-y-2 text-xs font-medium text-ivory-dim">
              <li>
                <Link to="/login" className="hover:text-white transition-colors">Login</Link>
              </li>
              <li>
                <Link to="/signup" className="hover:text-white transition-colors">Sign Up</Link>
              </li>
              <li>
                <Link to="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link>
              </li>
            </ul>
          </div>

        </div>

        {/* Copyright Bottom */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-ivory-dim font-normal">
          <p>© 2026 Team Jagruk Swadesh. All rights reserved.</p>
          <div className="flex items-center space-x-6 mt-4 sm:mt-0">
            <span>Built for Indian Standards Awareness</span>
            <Link to="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
