import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Sparkles, 
  ArrowRight, 
  BookOpen, 
  Award, 
  FlaskConical, 
  UserCheck, 
  Search, 
  BrainCircuit, 
  CheckCircle2, 
  Shield, 
  FileText, 
  Layers, 
  HelpCircle,
  ArrowUpRight
} from 'lucide-react';
import PageTransition from '../components/PageTransition';
import SectionHeading from '../components/SectionHeading';
import LiquidCard from '../components/LiquidCard';
import Button from '../components/Button';
import Logo from '../components/Logo';
import { useAuth } from '../context/AuthContext';

export default function Home({ onOpenChatbotModal }) {
  const { isAuthenticated } = useAuth();
  // 4 Main Helps With Domains
  const helpsWithDomains = [
    {
      icon: BookOpen,
      title: "Indian Standards",
      desc: "Explore and understand relevant Indian Standards across manufacturing, IT, consumer goods, and safety specifications.",
      link: "/explore"
    },
    {
      icon: Award,
      title: "Certification",
      desc: "Understand BIS ISI certification schemes, registration processes, mandatory compliance, and mark usage requirements.",
      link: "/explore"
    },
    {
      icon: FlaskConical,
      title: "Testing",
      desc: "Explore testing requirements, recognized laboratory networks, sample preparation, and testing methodology guidance.",
      link: "/explore"
    },
    {
      icon: UserCheck,
      title: "Consumer Guidance",
      desc: "Understand complex BIS-related consumer safety regulations, complaint registration, and standard verification.",
      link: "/explore"
    }
  ];

  // 3-Step Flow
  const steps = [
    {
      num: "01",
      title: "Ask",
      desc: "Describe what you need in simple language without needing to know technical standard numbers.",
      icon: Search
    },
    {
      num: "02",
      title: "Understand",
      desc: "Get relevant BIS information translated into clear, structured, and easy-to-digest formats.",
      icon: BrainCircuit
    },
    {
      num: "03",
      title: "Act",
      desc: "Use verified, source-backed insights to make compliance, manufacturing, or purchasing decisions.",
      icon: CheckCircle2
    }
  ];

  // 4 Core Pillars
  const whyPillars = [
    {
      title: "Relevant Information",
      desc: "Filtered to answer your specific compliance or consumer inquiry accurately without overwhelming noise.",
      icon: Layers
    },
    {
      title: "Source-Backed Knowledge",
      desc: "Grounded in official Bureau of Indian Standards guidelines, gazette notifications, and published norms.",
      icon: FileText
    },
    {
      title: "Easier Understanding",
      desc: "Transforms dense legal and technical standard documents into plain, structured Indian context.",
      icon: Sparkles
    },
    {
      title: "Centralized Access",
      desc: "Single unified interface for certification schemes, laboratory testing, consumer guidance, and standards.",
      icon: Shield
    }
  ];

  return (
    <PageTransition>
      <div className="space-y-24 sm:space-y-32 pt-28 pb-16">
        
        {/* HERO SECTION — REFERENCE COMPOSITION MATCH */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto pt-4 sm:pt-10">
          
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
            
            {/* HERO LEFT SIDE — TYPOGRAPHY & CAPSULE BUTTONS */}
            <motion.div 
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="lg:col-span-7 space-y-6 text-left"
            >
              {/* Eyebrow Label Tag (Reference Inspired) */}
              <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-forest-deep/80 border border-white/15 text-ivory-dim text-xs font-medium tracking-wide">
                <span className="text-emerald-400 font-bold">+</span>
                <span className="uppercase tracking-widest text-[11px] font-semibold text-ivory-muted">
                  BIS • COMPLIANCE • INTELLIGENCE
                </span>
              </div>

              {/* Two-Tone Display Heading (Reference Inspired) */}
              <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.08] text-white drop-shadow-[0_2px_10px_rgba(0,0,0,0.5)]">
                Understand <span className="text-saffron-light">Indian</span> <br />
                <span className="text-[#204028] sm:text-[#1c3a23] font-extrabold drop-shadow-sm">
                  Standards easily.
                </span>
              </h1>

              {/* Muted Subtitle */}
              <p className="text-base sm:text-lg text-[#1e3826] sm:text-ivory-muted max-w-xl leading-relaxed font-medium">
                Discover and understand BIS standards, certification, testing, and consumer guidance through one calm, intelligent platform.
              </p>

              {/* Action Buttons (Reference Pill Buttons) */}
              <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3.5 pt-3">
                <Link to={isAuthenticated ? "/chatbot" : "/signup"} className="w-full sm:w-auto">
                  <Button
                    variant="primary"
                    size="lg"
                    icon={ArrowRight}
                    className="w-full sm:w-auto"
                  >
                    Get Started
                  </Button>
                </Link>
                <Link to="/explore" className="w-full sm:w-auto">
                  <Button
                    variant="secondary"
                    size="lg"
                    className="w-full sm:w-auto"
                  >
                    Explore BIS Services
                  </Button>
                </Link>
              </div>
            </motion.div>


            {/* HERO RIGHT SIDE — FLOATING CARD WITH 3D ORB GRAPHIC (MATCHING REFERENCE "NATURE TODAY") */}
            <motion.div
              initial={{ opacity: 0, scale: 0.96, y: 15 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="lg:col-span-5"
            >
              <div className="liquid-glass-panel p-6 sm:p-7 space-y-5 border-white/15 relative">
                
                {/* Panel Top Header */}
                <div className="flex items-center justify-between pb-3 border-b border-white/10 text-xs font-semibold text-ivory-dim tracking-wider uppercase">
                  <span>JAGRUK SWADESH</span>
                  <div className="flex items-center space-x-1.5 text-emerald-400">
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                    <span className="text-[10px]">LIVE</span>
                  </div>
                </div>

                {/* Card Title */}
                <div className="space-y-0.5">
                  <h3 className="text-2xl font-bold text-white tracking-tight">
                    Indian Standards Today
                  </h3>
                  <p className="text-xs text-ivory-dim font-medium">
                    Integrated knowledge ecosystem for BIS services.
                  </p>
                </div>

                {/* Central 3D Orb Render Graphic */}
                <div className="py-4 flex justify-center items-center">
                  <div className="ecosystem-orb">
                    <div className="ecosystem-orb-ring" />
                    <div className="ecosystem-orb-ring-inner" />
                    <Logo size="sm" showText={false} />
                  </div>
                </div>

                {/* 2-Grid Metric Chips (Reference Style) */}
                <div className="grid grid-cols-2 gap-3 pt-1">
                  <div className="p-3 rounded-xl bg-forest-dark/80 border border-white/10 space-y-1">
                    <span className="text-[10px] uppercase font-semibold text-ivory-dim block">COVERAGE</span>
                    <p className="text-sm font-bold text-white">21,000+ IS Codes</p>
                  </div>

                  <div className="p-3 rounded-xl bg-forest-dark/80 border border-white/10 space-y-1">
                    <span className="text-[10px] uppercase font-semibold text-ivory-dim block">SCHEMES</span>
                    <p className="text-sm font-bold text-white">ISI & CRS Marks</p>
                  </div>
                </div>

                {/* Bottom Action Button (Reference Style) */}
                <button
                  onClick={onOpenChatbotModal}
                  className="w-full py-3 px-4 rounded-xl bg-forest-dark/90 hover:bg-forest-olive border border-white/12 hover:border-white/25 text-white font-semibold text-xs flex items-center justify-center space-x-2 transition-all group"
                >
                  <span>Query AI Chatbot</span>
                  <ArrowUpRight className="w-3.5 h-3.5 opacity-70 group-hover:opacity-100 transition-opacity" />
                </button>

              </div>
            </motion.div>

          </div>
        </section>


        {/* WHAT JAGRUK SWADESH HELPS WITH */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
          <SectionHeading
            tag="CORE COVERAGE"
            title="What Jagruk Swadesh Helps With"
            subtitle="Simplified discovery across all key domains of the Bureau of Indian Standards."
          />

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            {helpsWithDomains.map((domain, index) => {
              const IconComp = domain.icon;
              return (
                <Link key={index} to={domain.link} className="block group">
                  <LiquidCard className="h-full flex flex-col justify-between space-y-5">
                    <div className="space-y-3.5">
                      <div className="w-11 h-11 rounded-xl bg-forest-dark/90 border border-white/15 flex items-center justify-center text-emerald-300 group-hover:border-emerald-400/40 transition-all">
                        <IconComp className="w-5 h-5" />
                      </div>
                      <h3 className="text-xl font-bold text-white group-hover:text-emerald-200 transition-colors">
                        {domain.title}
                      </h3>
                      <p className="text-xs sm:text-sm text-ivory-muted leading-relaxed font-normal">
                        {domain.desc}
                      </p>
                    </div>

                    <div className="flex items-center space-x-2 text-xs font-semibold text-emerald-300 pt-2">
                      <span>Explore domain</span>
                      <ArrowRight className="w-3.5 h-3.5 transform group-hover:translate-x-1 transition-transform" />
                    </div>
                  </LiquidCard>
                </Link>
              );
            })}
          </div>
        </section>


        {/* HOW IT HELPS (3-STEP FLOW) */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
          <SectionHeading
            tag="SIMPLIFIED PROCESS"
            title="How It Helps"
            subtitle="From complex regulatory standards to clear, actionable guidance in three simple steps."
          />

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {steps.map((step, idx) => {
              const StepIcon = step.icon;
              return (
                <LiquidCard key={idx} className="h-full space-y-4 p-7">
                  <div className="flex items-center justify-between">
                    <span className="text-3xl font-extrabold text-emerald-300 tracking-tight">
                      {step.num}
                    </span>
                    <div className="w-9 h-9 rounded-xl bg-forest-dark/90 border border-white/15 flex items-center justify-center text-emerald-300">
                      <StepIcon className="w-4 h-4" />
                    </div>
                  </div>

                  <h3 className="text-xl font-bold text-white">{step.title}</h3>
                  <p className="text-xs sm:text-sm text-ivory-muted leading-relaxed font-normal">{step.desc}</p>
                </LiquidCard>
              );
            })}
          </div>
        </section>


        {/* WHY JAGRUK SWADESH */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
          <SectionHeading
            tag="KEY VALUES"
            title="Why Jagruk Swadesh"
            subtitle="Built on trust, source accuracy, and user clarity for Indian enterprises and consumers."
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {whyPillars.map((pillar, idx) => {
              const PillarIcon = pillar.icon;
              return (
                <LiquidCard key={idx} className="flex items-start space-x-4 p-6">
                  <div className="w-11 h-11 rounded-xl bg-forest-dark/90 border border-white/15 flex items-center justify-center text-emerald-300 shrink-0 mt-0.5">
                    <PillarIcon className="w-5 h-5" />
                  </div>
                  <div className="space-y-1.5">
                    <h3 className="text-lg font-bold text-white">{pillar.title}</h3>
                    <p className="text-xs sm:text-sm text-ivory-muted leading-relaxed font-normal">{pillar.desc}</p>
                  </div>
                </LiquidCard>
              );
            })}
          </div>
        </section>


        {/* FINAL CTA SECTION */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <div className="liquid-glass-panel p-8 sm:p-12 text-center space-y-5 border-white/15 relative overflow-hidden">
            <div className="w-14 h-14 rounded-2xl bg-forest-dark/90 border border-white/15 flex items-center justify-center text-emerald-300 mx-auto">
              <HelpCircle className="w-7 h-7" />
            </div>

            <div className="max-w-xl mx-auto space-y-2">
              <h2 className="text-2xl sm:text-3xl font-extrabold text-white">
                Have a question about BIS?
              </h2>
              <p className="text-sm text-ivory-muted font-normal">
                Explore Jagruk Swadesh or ask the intelligent assistant directly.
              </p>
            </div>

            <div className="pt-2">
              <Button
                variant="primary"
                size="lg"
                icon={Sparkles}
                onClick={onOpenChatbotModal}
                className="mx-auto"
              >
                Launch AI Chatbot
              </Button>
            </div>
          </div>
        </section>

      </div>
    </PageTransition>
  );
}
