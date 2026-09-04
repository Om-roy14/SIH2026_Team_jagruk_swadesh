import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Shield, ChevronDown, ChevronUp, Lock } from 'lucide-react';
import PageTransition from '../components/PageTransition';
import SectionHeading from '../components/SectionHeading';

export default function PrivacyPolicy() {
  const [openAccordion, setOpenAccordion] = useState(null);

  const sections = [
    {
      id: 'collection',
      title: '1. Information We Collect',
      content: 'We collect minimal user information necessary to provide standardized BIS inquiry guidance. This includes account credentials (name, email) provided during signup, and interaction metadata during platform queries.'
    },
    {
      id: 'usage',
      title: '2. How Information Is Used',
      content: 'Information is utilized strictly to deliver accurate Indian Standards guidance, maintain platform security, improve search accuracy across BIS domains, and communicate essential system alerts.'
    },
    {
      id: 'account',
      title: '3. Account Information',
      content: 'Your account credentials are stored in encrypted form. We do not sell, rent, or trade user account details to third parties for marketing purposes.'
    },
    {
      id: 'chat-data',
      title: '4. Chat / Interaction Data',
      content: 'Queries submitted through the "Jagruk Swadesh AI Chatbot" entry point are processed to formulate source-grounded answers. Interaction logs are anonymized and retained solely for platform refinement.'
    },
    {
      id: 'security',
      title: '5. Data Security',
      content: 'We employ physical, technical, and administrative safeguards including SSL/TLS encryption, restricted database access, and continuous monitoring to protect user information.'
    },
    {
      id: 'cookies',
      title: '6. Cookies & Local Storage',
      content: 'Essential session cookies are used to keep you authenticated and store layout preferences. No intrusive tracking or advertising cookies are deployed.'
    },
    {
      id: 'rights',
      title: '7. User Rights',
      content: 'You retain full rights to request access to, correction of, or complete deletion of your account data by contacting Team Jagruk Swadesh support.'
    },
    {
      id: 'updates',
      title: '8. Policy Updates',
      content: 'We may update this Privacy Policy periodically to reflect changes in regulatory compliance or system enhancements. Significant updates will be highlighted on the platform.'
    },
    {
      id: 'contact',
      title: '9. Contact Us',
      content: 'If you have questions regarding this Privacy Policy or data governance practices, please reach out to Team Jagruk Swadesh at privacy@jagruk-swadesh.in.'
    }
  ];

  return (
    <PageTransition>
      <div className="space-y-12 sm:space-y-16 pt-28 pb-16">
        
        {/* Header */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto text-center space-y-4">
          <SectionHeading
            tag="LEGAL GOVERNANCE"
            title="Privacy Policy"
            subtitle="Prioritizing data transparency, security, and user trust."
          />
          <div className="inline-flex items-center space-x-2 text-xs text-ivory-dim pt-1">
            <Lock className="w-3.5 h-3.5 text-emerald-400" />
            <span>Last Updated: September 2026</span>
          </div>
        </section>

        {/* Content Panel */}
        <section className="px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
          <div className="liquid-glass-panel p-6 sm:p-10 space-y-8 border-white/12">
            
            <p className="text-xs sm:text-sm text-ivory-muted leading-relaxed border-b border-white/10 pb-6 font-normal">
              Team Jagruk Swadesh is committed to protecting your privacy. This policy outlines how we handle personal information, query interaction logs, and data security when you interact with our platform for Indian Standards and BIS services.
            </p>

            {/* Accordion List */}
            <div className="space-y-3">
              {sections.map((section) => (
                <div 
                  key={section.id} 
                  className="rounded-xl bg-forest-dark/80 border border-white/10 overflow-hidden transition-colors hover:border-white/20"
                >
                  <button
                    onClick={() => setOpenAccordion(openAccordion === section.id ? null : section.id)}
                    className="w-full px-5 py-3.5 flex items-center justify-between text-left font-semibold text-white text-sm sm:text-base focus:outline-none"
                  >
                    <span>{section.title}</span>
                    {openAccordion === section.id ? (
                      <ChevronUp className="w-4 h-4 text-emerald-300 shrink-0" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-ivory-dim shrink-0" />
                    )}
                  </button>

                  <motion.div
                    initial={false}
                    animate={{ height: openAccordion === section.id ? 'auto' : 0, opacity: openAccordion === section.id ? 1 : 0 }}
                    transition={{ duration: 0.2 }}
                    className="overflow-hidden"
                  >
                    <div className="px-5 pb-4 pt-1 text-xs sm:text-sm text-ivory-muted leading-relaxed font-normal border-t border-white/5">
                      {section.content}
                    </div>
                  </motion.div>
                </div>
              ))}
            </div>

            {/* Bottom Assurance */}
            <div className="pt-6 border-t border-white/10 flex items-center space-x-3 text-xs text-ivory-dim">
              <Shield className="w-4.5 h-4.5 text-emerald-400 shrink-0" />
              <span>Compliant with Indian digital data protection standards and Bureau guidelines.</span>
            </div>

          </div>
        </section>

      </div>
    </PageTransition>
  );
}
