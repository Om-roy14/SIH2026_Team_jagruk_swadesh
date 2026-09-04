import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BookOpen, 
  Award, 
  FlaskConical, 
  UserCheck, 
  ArrowRight, 
  CheckCircle2, 
  Sparkles 
} from 'lucide-react';
import PageTransition from '../components/PageTransition';
import SectionHeading from '../components/SectionHeading';
import LiquidCard from '../components/LiquidCard';
import Button from '../components/Button';

export default function Explore({ onOpenChatbotModal }) {
  const [activeTab, setActiveTab] = useState('all');

  const services = [
    {
      id: 'standards',
      category: 'standards',
      icon: BookOpen,
      title: 'Indian Standards (IS)',
      shortDesc: 'Discover and understand relevant Indian Standards across manufacturing, safety, and IT.',
      fullDesc: 'The Bureau of Indian Standards formulates Indian Standards across 15 sectors including Chemical, Food & Agriculture, Civil Engineering, Electronics, and Textiles. Jagruk Swadesh simplifies technical terminology into practical specifications.',
      highlights: [
        'Over 21,000+ formulated Indian Standards simplified',
        'Sectoral categorization & cross-reference lookup',
        'Quality specifications for raw materials & finished goods',
        'Technical committee guidelines explained'
      ]
    },
    {
      id: 'certification',
      category: 'certification',
      icon: Award,
      title: 'BIS Certification',
      shortDesc: 'Understand BIS certification schemes, ISI mark usage, and registration processes.',
      fullDesc: 'BIS operates Product Certification Schemes granting licenses to manufacturers to use the iconic ISI mark, as well as the Compulsory Registration Scheme (CRS) for electronic items.',
      highlights: [
        'ISI Mark License Application Workflow',
        'Compulsory Registration Scheme (CRS) compliance',
        'Foreign Manufacturers Certification Scheme (FMCS)',
        'Factory audit & surveillance protocol details'
      ]
    },
    {
      id: 'testing',
      category: 'testing',
      icon: FlaskConical,
      title: 'Testing & Laboratories',
      shortDesc: 'Explore testing-related information, recognized laboratory networks, and parameters.',
      fullDesc: 'Central Laboratory & Regional Laboratory Networks test products against Indian Standard requirements to ensure public safety, durability, and performance compliance.',
      highlights: [
        'Central, Regional, & Branch Laboratory Directory',
        'LIMS (Laboratory Information Management System) guidance',
        'Sample submission rules & turnaround timelines',
        'Recognized third-party private testing lab accreditation'
      ]
    },
    {
      id: 'consumer',
      category: 'consumer',
      icon: UserCheck,
      title: 'Consumer Guidance',
      shortDesc: 'Access BIS-related consumer information, complaint redressal, and awareness.',
      fullDesc: 'Empowering everyday Indian consumers to verify genuine ISI marks, report counterfeit products, understand recall advisories, and access safety guidelines.',
      highlights: [
        'BIS CARE App feature walkthrough & verification tips',
        'Rights against non-standard or defective products',
        'Reporting fake ISI marks & non-certified goods',
        'Public interest standard alerts & awareness campaigns'
      ]
    }
  ];

  const filteredServices = activeTab === 'all' 
    ? services 
    : services.filter(s => s.category === activeTab);

  return (
    <PageTransition>
      <div className="space-y-16 sm:space-y-24 pt-28 pb-16">
        
        {/* Explore Hero Header */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto text-center space-y-6">
          <SectionHeading
            tag="KNOWLEDGE BASE"
            title="Explore BIS Services"
            subtitle="Discover information across major Bureau of Indian Standards domains."
          />

          {/* Reference Matched Capsule Filter Tabs */}
          <div className="flex flex-wrap items-center justify-center gap-2 max-w-4xl mx-auto pt-2">
            {[
              { id: 'all', label: 'All Services' },
              { id: 'standards', label: 'Indian Standards' },
              { id: 'certification', label: 'Certification' },
              { id: 'testing', label: 'Testing & Labs' },
              { id: 'consumer', label: 'Consumer Guidance' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4.5 py-2 text-xs sm:text-sm font-semibold rounded-full transition-all duration-200 ${
                  activeTab === tab.id
                    ? 'btn-pill-primary text-white shadow-md'
                    : 'btn-pill-secondary text-ivory-muted hover:text-white'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </section>


        {/* Service Cards Grid */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-7">
            <AnimatePresence mode="popLayout">
              {filteredServices.map(service => {
                const IconComponent = service.icon;
                return (
                  <motion.div
                    key={service.id}
                    layout
                    initial={{ opacity: 0, scale: 0.96 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.96 }}
                    transition={{ duration: 0.25 }}
                  >
                    <LiquidCard className="h-full flex flex-col justify-between space-y-6 p-7 border-white/12">
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <div className="w-11 h-11 rounded-xl bg-forest-dark/90 border border-white/15 flex items-center justify-center text-emerald-300">
                            <IconComponent className="w-5.5 h-5.5" />
                          </div>
                          <span className="px-3 py-1 rounded-full bg-forest-dark/80 border border-white/12 text-[10px] font-semibold uppercase tracking-wider text-emerald-300">
                            {service.category}
                          </span>
                        </div>

                        <h3 className="text-2xl font-bold text-white">{service.title}</h3>
                        <p className="text-xs sm:text-sm text-ivory-muted leading-relaxed font-normal">{service.fullDesc}</p>

                        <div className="pt-2 space-y-2">
                          <span className="text-[11px] font-semibold text-emerald-300 uppercase tracking-wider block">Key Aspects</span>
                          <ul className="space-y-2">
                            {service.highlights.map((h, i) => (
                              <li key={i} className="flex items-start space-x-2 text-xs text-ivory-dim font-medium">
                                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                                <span>{h}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>

                      <div className="pt-4 border-t border-white/10 flex items-center justify-between">
                        <span className="text-[11px] text-ivory-dim font-medium">Source-backed guidance</span>
                        <button
                          onClick={onOpenChatbotModal}
                          className="inline-flex items-center space-x-1.5 text-xs font-semibold text-emerald-300 hover:text-white transition-colors"
                        >
                          <span>Ask AI Chatbot about this</span>
                          <ArrowRight className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </LiquidCard>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>
        </section>


        {/* Explore Interactive Prompt Banner */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <div className="liquid-glass-panel p-8 sm:p-10 flex flex-col md:flex-row items-center justify-between gap-6 border-white/15">
            <div className="space-y-1 text-center md:text-left">
              <h3 className="text-xl sm:text-2xl font-bold text-white">
                Need specific standard details or IS codes?
              </h3>
              <p className="text-xs sm:text-sm text-ivory-muted font-normal">
                Use Jagruk Swadesh to query exact compliance guidelines or testing limits.
              </p>
            </div>
            <Button
              variant="primary"
              size="md"
              icon={Sparkles}
              onClick={onOpenChatbotModal}
              className="shrink-0"
            >
              Try AI Chatbot
            </Button>
          </div>
        </section>

      </div>
    </PageTransition>
  );
}
