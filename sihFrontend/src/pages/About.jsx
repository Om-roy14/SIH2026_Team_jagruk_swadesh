import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Database, 
  Cpu, 
  Sparkles, 
  Lightbulb, 
  CheckCircle,
  FileSearch,
  Target,
  Shield,
  Search,
  BookOpen,
  User,
  X
} from 'lucide-react';
import PageTransition from '../components/PageTransition';
import SectionHeading from '../components/SectionHeading';
import LiquidCard from '../components/LiquidCard';
import Logo from '../components/Logo';
import Button from '../components/Button';

export default function About({ onOpenChatbotModal }) {
  // Active selected member index (default to null: ALL 6 members compact initially)
  const [selectedMember, setSelectedMember] = useState(null);

  // Exact 6 Team Members in Strict Sequence
  const teamMembers = [
    {
      id: 1,
      name: "Om Kumar Roy",
      role: "Team Lead & AI Assistant Architect",
      description: "Architecting the brains of our platform. Specializing in AI pipelines, backend engineering, and leading our crew from concept to deployment.",
      image: "/team/om-kumar-roy.jpg",
      initials: "OR"
    },
    {
      id: 2,
      name: "Om Jee",
      role: "Frontend Architect",
      description: "Building the face of the platform. Specializing in modern frameworks and polished UI components to turn wireframes into a pixel-perfect, dynamic web experience.",
      image: "/team/om-jee.jpg",
      initials: "OJ"
    },
    {
      id: 3,
      name: "Videesh Sharma",
      role: "Backend Integration",
      description: "Wiring up the interface. Specializing in UI backend architecture and API integration to ensure the frontend communicates flawlessly with our complex machine learning models.",
      image: "/team/videesh-sharma.jpg",
      initials: "VS"
    },
    {
      id: 4,
      name: "Saurabh Devliyal",
      role: "Frontend QA & Documentation",
      description: "Polishing the final experience. Specializing in frontend quality assurance, UX and performance testing, interface validation, and documenting the technical journey behind our platform.",
      image: "/team/saurav-devliyal.jpg",
      initials: "SD"
    },
    {
      id: 5,
      name: "Shruti Yadav",
      role: "Research Specialist",
      description: "Decoding the challenge. Specializing in domain research and problem-statement analysis to build the strategic foundation that our entire pipeline rests on.",
      image: "/team/shruti-yadav.jpg",
      initials: "SY"
    },
    {
      id: 6,
      name: "Sonu Kumar",
      role: "Research Specialist",
      description: "Decoding the problem statement. Specializing in deep-dive research, domain analysis, and establishing the foundational blueprint that guided our development.",
      image: "/team/sonu-kumar.jpg",
      initials: "SK"
    }
  ];

  // Key Aims List
  const aimsList = [
    "Easier discovery of Indian Standards",
    "Better understanding of BIS services",
    "Guidance around certification requirements",
    "Access to relevant testing information",
    "Source-backed information",
    "A simpler conversational experience"
  ];

  // Target User Groups
  const targetAudience = [
    "MSMEs",
    "Startups",
    "Industries",
    "Students",
    "Consumers"
  ];

  // How It Works 4-Step Flow
  const flowSteps = [
    {
      stage: "01",
      title: "BIS Knowledge Sources",
      desc: "Aggregating official Indian Standards, certification protocols, and testing documentation.",
      icon: Database
    },
    {
      stage: "02",
      title: "Information Processing",
      desc: "Structuring dense technical specifications and regulatory text into readable intelligence.",
      icon: Cpu
    },
    {
      stage: "03",
      title: "Intelligent Retrieval",
      desc: "Searching exact standard references grounded strictly in official source guidelines.",
      icon: Search
    },
    {
      stage: "04",
      title: "Simple User Experience",
      desc: "Delivering clear, plain-language answers directly to users over our crystal-clear interface.",
      icon: Sparkles
    }
  ];

  return (
    <PageTransition>
      <div className="space-y-24 sm:space-y-32 pt-28 pb-16">
        
        {/* HERO SECTION — ABOUT JAGRUK SWADESH WITH HIGH-CONTRAST BACKDROP */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-8">
          <div className="flex justify-center pb-2">
            <Logo size="lg" />
          </div>
          
          <div className="text-center max-w-4xl mx-auto space-y-5 px-6 sm:px-8 py-7 sm:py-9 rounded-3xl bg-forest-dark/90 backdrop-blur-md border border-white/12 shadow-xl">
            <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-forest-deep/90 border border-white/15 text-ivory-dim text-xs font-medium tracking-wide">
              <span className="text-emerald-400 font-bold">+</span>
              <span className="uppercase tracking-widest text-[11px] font-semibold text-ivory-muted">
                OUR MISSION & PURPOSE
              </span>
            </div>

            <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight">
              About <span className="text-emerald-300">Jagruk Swadesh</span>
            </h1>

            <p className="text-sm sm:text-base text-ivory-muted leading-relaxed font-medium max-w-2xl mx-auto">
              Jagruk Swadesh is an AI-powered intelligent assistant designed to make Indian Standards and BIS-related information easier to discover, understand and use.
            </p>
          </div>

          <div className="liquid-glass-panel p-7 sm:p-10 border-white/12 max-w-4xl mx-auto text-center space-y-4">
            <p className="text-sm sm:text-base text-ivory-muted leading-relaxed font-normal">
              The platform addresses the difficulty users face when information is distributed across standards, documents, certification resources, testing information and other BIS services.
            </p>
            <p className="text-sm sm:text-base text-emerald-300 leading-relaxed font-semibold">
              Jagruk Swadesh aims to bring this information into a simpler conversational experience so that industries, MSMEs, startups, students and consumers can find relevant information more efficiently.
            </p>
          </div>
        </section>


        {/* THE PROBLEM & OUR SOLUTION */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-7">
            
            {/* The Problem Card */}
            <LiquidCard className="space-y-6 p-7 sm:p-8 border-red-500/20 hover:border-red-500/40 flex flex-col justify-between">
              <div className="space-y-5">
                <div className="w-11 h-11 rounded-xl bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-400">
                  <FileSearch className="w-5.5 h-5.5" />
                </div>

                <div className="space-y-2">
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-red-400 bg-forest-dark/80 px-3 py-1 rounded-full border border-red-500/20">
                    THE PROBLEM
                  </span>
                  <h3 className="text-2xl sm:text-3xl font-bold text-white">
                    Scattered BIS Resources
                  </h3>
                </div>

                <p className="text-xs sm:text-sm text-ivory-muted leading-relaxed font-normal">
                  BIS publishes a large amount of information covering Indian Standards, certification, testing, conformity assessment and consumer-related services. Finding the right information can require users to search through multiple documents, portals and technical resources.
                </p>
              </div>

              <div className="pt-5 border-t border-white/10 space-y-2.5">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-red-400 block">
                  Especially Difficult For:
                </span>
                <div className="flex flex-wrap gap-2">
                  {targetAudience.map((group, idx) => (
                    <span 
                      key={idx}
                      className="px-3 py-1 rounded-lg bg-forest-dark/80 border border-white/10 text-xs font-medium text-ivory-muted"
                    >
                      {group}
                    </span>
                  ))}
                </div>
              </div>
            </LiquidCard>

            {/* Our Solution Card */}
            <LiquidCard className="space-y-6 p-7 sm:p-8 border-white/15 flex flex-col justify-between">
              <div className="space-y-5">
                <div className="w-11 h-11 rounded-xl bg-forest-dark/90 border border-white/15 flex items-center justify-center text-emerald-300">
                  <Lightbulb className="w-5.5 h-5.5" />
                </div>

                <div className="space-y-2">
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-emerald-300 bg-forest-dark/80 px-3 py-1 rounded-full border border-white/12">
                    OUR SOLUTION
                  </span>
                  <h3 className="text-2xl sm:text-3xl font-bold text-white">
                    Natural Language Pipeline
                  </h3>
                </div>

                <p className="text-xs sm:text-sm text-ivory-muted leading-relaxed font-normal">
                  Jagruk Swadesh uses an intelligent information pipeline to help users interact with BIS-related knowledge using natural language. Users can describe what they need in simple language and the platform can help them discover relevant information from its knowledge sources.
                </p>
              </div>

              <div className="pt-5 border-t border-white/10 space-y-2">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-emerald-300 block">
                  Core Advantage:
                </span>
                <div className="flex items-center space-x-2 text-xs font-medium text-ivory-muted">
                  <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span>Translates dense standard requirements into plain, actionable Indian context.</span>
                </div>
              </div>
            </LiquidCard>

          </div>
        </section>


        {/* WHAT WE AIM TO PROVIDE & OUR VISION */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-7 items-stretch">
            
            {/* What We Aim To Provide (7 Columns) */}
            <div className="lg:col-span-7 liquid-glass-panel p-7 sm:p-9 space-y-5 border-white/12">
              <div className="flex items-center space-x-3">
                <div className="w-9 h-9 rounded-xl bg-forest-dark/90 border border-white/15 flex items-center justify-center text-emerald-300">
                  <Target className="w-4.5 h-4.5" />
                </div>
                <h3 className="text-2xl font-bold text-white">
                  What We Aim To Provide
                </h3>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-1">
                {aimsList.map((aim, idx) => (
                  <div 
                    key={idx}
                    className="p-3.5 rounded-xl bg-forest-dark/80 border border-white/10 flex items-start space-x-2.5"
                  >
                    <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                    <span className="text-xs sm:text-sm font-medium text-white leading-snug">{aim}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Our Vision (5 Columns) */}
            <div className="lg:col-span-5 liquid-glass-panel p-7 sm:p-9 space-y-5 border-white/15 flex flex-col justify-between">
              <div className="space-y-4">
                <div className="w-9 h-9 rounded-xl bg-forest-dark/90 border border-white/15 flex items-center justify-center text-emerald-300">
                  <BookOpen className="w-4.5 h-4.5" />
                </div>
                <span className="text-[11px] font-semibold uppercase tracking-wider text-emerald-300 block">
                  THE FUTURE
                </span>
                <h3 className="text-2xl font-bold text-white">
                  Our Vision
                </h3>
                <p className="text-base sm:text-lg text-ivory-muted leading-relaxed font-normal pt-1">
                  "Make reliable information about Indian Standards and BIS services easier for people to discover and understand."
                </p>
              </div>

              <div className="pt-5 border-t border-white/10">
                <Button
                  variant="primary"
                  size="md"
                  icon={Sparkles}
                  onClick={onOpenChatbotModal}
                  className="w-full"
                >
                  Launch AI Chatbot
                </Button>
              </div>
            </div>

          </div>
        </section>


        {/* HOW IT WORKS — VISUAL FLOW */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
          <SectionHeading
            tag="VISUAL PIPELINE"
            title="How It Works"
            subtitle="An end-to-end intelligent pipeline transforming standards into clear user answers."
          />

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 relative">
            {flowSteps.map((step, idx) => {
              const StepIcon = step.icon;
              return (
                <LiquidCard key={idx} className="h-full space-y-4 p-6 flex flex-col justify-between">
                  <div className="space-y-3.5">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-semibold uppercase tracking-widest text-emerald-300 bg-forest-dark/80 px-2.5 py-1 rounded-full border border-white/10">
                        STAGE {step.stage}
                      </span>
                      <div className="w-9 h-9 rounded-xl bg-forest-dark/90 border border-white/15 flex items-center justify-center text-emerald-300">
                        <StepIcon className="w-4 h-4" />
                      </div>
                    </div>

                    <h4 className="text-lg font-bold text-white">
                      {step.title}
                    </h4>
                    <p className="text-xs text-ivory-muted leading-relaxed font-normal">
                      {step.desc}
                    </p>
                  </div>
                </LiquidCard>
              );
            })}
          </div>
        </section>


        {/* TEAM JAGRUK SWADESH — WITH EXPLICIT COLLAPSE OPTION ON EXPANDED MEMBER */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto space-y-12">
          <SectionHeading
            tag="THE BUILDERS"
            title="Meet Team Jagruk Swadesh"
            subtitle="Six minds working across research, intelligence, engineering, design and quality to build a simpler way to access BIS knowledge."
          />

          {/* DESKTOP & TABLET LINEAR SHOWCASE */}
          <div className="hidden md:flex items-stretch gap-3.5 overflow-x-auto py-3 px-1 min-h-[420px]">
            {teamMembers.map((member, index) => {
              const isSelected = selectedMember === index;
              return (
                <motion.div
                  key={member.id}
                  layout
                  onClick={() => setSelectedMember(isSelected ? null : index)}
                  transition={{ type: "spring", stiffness: 300, damping: 26 }}
                  className={`cursor-pointer rounded-2xl relative transition-all duration-300 flex flex-col justify-between p-5 border ${
                    isSelected
                      ? 'flex-[2.2] bg-forest-deep/95 border-emerald-400/60 shadow-xl ring-1 ring-emerald-400/40'
                      : 'flex-1 bg-forest-dark/80 hover:bg-forest-deep/80 border-white/12 hover:border-white/25'
                  }`}
                >
                  {/* Top Badge with Collapse Button when Selected */}
                  <div className="flex items-center justify-between pb-3 border-b border-white/10">
                    <span className={`text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full ${
                      isSelected 
                        ? 'bg-emerald-400/20 border border-emerald-400/40 text-emerald-300' 
                        : 'bg-white/5 text-ivory-dim'
                    }`}>
                      0{member.id}
                    </span>
                    {isSelected && (
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedMember(null);
                        }}
                        className="text-[10px] font-semibold text-emerald-300 hover:text-white uppercase tracking-wider bg-emerald-400/20 hover:bg-emerald-400/30 px-2.5 py-0.5 rounded-full border border-emerald-400/40 flex items-center space-x-1 transition-colors"
                        title="Collapse member details"
                      >
                        <X className="w-3 h-3" />
                        <span>Collapse</span>
                      </button>
                    )}
                  </div>

                  {/* Profile Photo Area */}
                  <div className="py-3 flex flex-col items-center justify-center text-center space-y-2.5">
                    <div className={`relative rounded-2xl overflow-hidden border transition-all duration-300 shadow-md ${
                      isSelected 
                        ? 'w-28 h-28 border-emerald-400/60' 
                        : 'w-18 h-18 border-white/20'
                    }`}>
                      {member.image ? (
                        <img 
                          src={member.image} 
                          alt={member.name}
                          className="w-full h-full object-cover object-top"
                        />
                      ) : (
                        <div className="w-full h-full bg-forest-dark flex flex-col items-center justify-center text-emerald-300 border border-white/10 p-2">
                          <User className="w-8 h-8 mb-1 opacity-70" />
                          <span className="text-xs font-bold tracking-widest">{member.initials}</span>
                        </div>
                      )}
                    </div>

                    <div className="space-y-0.5">
                      <h4 className={`font-bold text-white transition-all ${
                        isSelected ? 'text-xl text-emerald-200' : 'text-sm'
                      }`}>
                        {member.name}
                      </h4>
                      <p className={`transition-all ${
                        isSelected ? 'text-xs font-medium text-emerald-400 uppercase tracking-wider' : 'text-[11px] font-normal text-ivory-dim'
                      }`}>
                        {member.role}
                      </p>
                    </div>
                  </div>

                  {/* Description — Prominent on Selected Member with explicit Collapse CTA */}
                  <div className="pt-3 border-t border-white/10 space-y-2">
                    {isSelected ? (
                      <>
                        <motion.p 
                          initial={{ opacity: 0, y: 4 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ duration: 0.2 }}
                          className="text-xs text-ivory-muted leading-relaxed font-normal text-center"
                        >
                          "{member.description}"
                        </motion.p>
                        <div className="flex justify-center pt-1">
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              setSelectedMember(null);
                            }}
                            className="inline-flex items-center space-x-1 text-[11px] font-semibold text-emerald-300 hover:text-white transition-colors"
                          >
                            <X className="w-3 h-3" />
                            <span>Collapse</span>
                          </button>
                        </div>
                      </>
                    ) : (
                      <p className="text-[10px] text-ivory-dim font-normal text-center">
                        Click to expand
                      </p>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </div>

          {/* MOBILE RESPONSIVE TEAM SHOWCASE */}
          <div className="md:hidden space-y-3">
            {teamMembers.map((member, index) => {
              const isSelected = selectedMember === index;
              return (
                <div
                  key={member.id}
                  onClick={() => setSelectedMember(isSelected ? null : index)}
                  className={`rounded-2xl p-4 border transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-forest-deep/95 border-emerald-400/60 shadow-md'
                      : 'bg-forest-dark/80 border-white/12'
                  }`}
                >
                  <div className="flex items-center space-x-3.5">
                    <div className="w-14 h-14 rounded-xl overflow-hidden border border-white/20 shrink-0">
                      {member.image ? (
                        <img 
                          src={member.image} 
                          alt={member.name}
                          className="w-full h-full object-cover object-top"
                        />
                      ) : (
                        <div className="w-full h-full bg-forest-dark flex flex-col items-center justify-center text-emerald-300">
                          <User className="w-5 h-5" />
                          <span className="text-[9px] font-bold">{member.initials}</span>
                        </div>
                      )}
                    </div>

                    <div className="space-y-0.5 flex-1">
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] font-semibold text-emerald-300 uppercase">
                          0{member.id} • {member.role}
                        </span>
                        {isSelected && (
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              setSelectedMember(null);
                            }}
                            className="text-[10px] font-semibold text-emerald-300 hover:text-white uppercase tracking-wider bg-emerald-400/20 px-2 py-0.5 rounded-full border border-emerald-400/40 flex items-center space-x-1"
                          >
                            <X className="w-3 h-3" />
                            <span>Collapse</span>
                          </button>
                        )}
                      </div>
                      <h4 className="text-base font-bold text-white">{member.name}</h4>
                      {!isSelected && (
                        <p className="text-[10px] text-ivory-dim font-normal">Click to expand</p>
                      )}
                    </div>
                  </div>

                  {isSelected && (
                    <motion.div 
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      transition={{ duration: 0.2 }}
                      className="pt-2.5 border-t border-white/10 mt-2.5 space-y-2"
                    >
                      <p className="text-xs text-ivory-muted leading-relaxed font-normal">
                        "{member.description}"
                      </p>
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedMember(null);
                        }}
                        className="inline-flex items-center space-x-1 text-[11px] font-semibold text-emerald-300 hover:text-white pt-1"
                      >
                        <X className="w-3 h-3" />
                        <span>Collapse member details</span>
                      </button>
                    </motion.div>
                  )}
                </div>
              );
            })}
          </div>
        </section>


        {/* FINAL CTA SECTION */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <div className="liquid-glass-panel p-8 sm:p-12 text-center space-y-5 border-white/15 relative">
            <div className="w-14 h-14 rounded-2xl bg-forest-dark/90 border border-white/15 flex items-center justify-center text-emerald-300 mx-auto">
              <Shield className="w-7 h-7" />
            </div>

            <div className="max-w-xl mx-auto space-y-2">
              <h2 className="text-2xl sm:text-3xl font-bold text-white">
                Ready to explore Indian Standards?
              </h2>
              <p className="text-sm text-ivory-muted font-normal">
                Start discovering BIS guidelines with Jagruk Swadesh assistant today.
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
