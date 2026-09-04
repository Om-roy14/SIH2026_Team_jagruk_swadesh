import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Sparkles, 
  X, 
  Send, 
  RefreshCw, 
  ShieldCheck, 
  FileText, 
  CheckCircle2,
  Bot,
  User,
  HelpCircle,
  BookOpen,
  ArrowRight
} from 'lucide-react';
import Logo from './Logo';

// Knowledge Base Pre-sets
const SUGGESTED_QUESTIONS = [
  {
    q: "What is IS 10500:2012 for Drinking Water?",
    category: "Indian Standards"
  },
  {
    q: "How to check genuine ISI mark on products?",
    category: "Consumer Guidance"
  },
  {
    q: "What is the process for BIS ISI Certification?",
    category: "Certification"
  },
  {
    q: "What testing is mandatory for Toy Safety (IS 9873)?",
    category: "Testing & Labs"
  }
];

const KNOWLEDGE_RESPONSES = {
  "water": {
    answer: "IS 10500:2012 defines the official Indian Standard for Drinking Water Specifications. It sets acceptable and permissible limits for physical, chemical, and bacteriological parameters. For example: pH must be between 6.5 to 8.5, Total Dissolved Solids (TDS) acceptable limit is 500 mg/l (permissible limit 2000 mg/l), Turbidity limit is 1 NTU, and E. coli bacteria must be completely absent.",
    sources: [
      "IS 10500:2012 — Drinking Water Specification (Second Revision)",
      "Table 1 & 2 — Organoleptic, Physical, and Chemical Limits",
      "Bureau of Indian Standards Quality Assessment Manual"
    ]
  },
  "consumer": {
    answer: "Every genuine ISI mark product features a CML (CM/L) license number directly below the ISI logo. Consumers can verify any CML number using the official 'BIS CARE' mobile app under 'Verify License Details'. It displays the manufacturer's name, registered factory address, validity status, and standard scope.",
    sources: [
      "Bureau of Indian Standards Consumer Protection Framework",
      "BIS CARE App Mobile Verification Guidelines",
      "Consumer Rights under BIS Conformity Regulations"
    ]
  },
  "certification": {
    answer: "The BIS ISI Mark Certification process under Scheme-I involves: 1) Identifying the relevant Indian Standard (IS code). 2) Submitting an online application on Manak Online with factory testing infrastructure details. 3) Preliminary factory audit by BIS officers. 4) Sample drawing for testing at BIS recognized labs. 5) Grant of license upon satisfactory audit and test reports.",
    sources: [
      "BIS Conformity Assessment Regulations 2018 — Scheme I",
      "Manak Online Portal Application Guidelines for Manufacturers",
      "IS/ISO 9001 Quality System Verification Criteria"
    ]
  },
  "toy": {
    answer: "Under the Toys (Quality Control) Order, all children's toys sold in India must bear the ISI mark compliant with IS 9873 standards. Mandatory safety tests include Mechanical & Physical Safety (IS 9873 Part 1 - sharp edges, small choke parts), Flammability Safety (Part 2), and Heavy Metal Toxicity Limits (Part 3 - testing for lead, cadmium, arsenic, and phthalate migration).",
    sources: [
      "IS 9873 (Parts 1-9) — Safety Requirements for Toys",
      "Toys (Quality Control) Order 2020 — Ministry of Commerce and Industry",
      "Central BIS Laboratory Testing Guidelines for Consumer Products"
    ]
  }
};

export default function ChatbotIntegrationModal({ isOpen, onClose }) {
  const [messages, setMessages] = useState([]);
  const [inputQuery, setInputQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto scroll to bottom of chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (messages.length > 0) {
      scrollToBottom();
    }
  }, [messages, isLoading]);

  if (!isOpen) return null;

  const handleSend = (queryToSend) => {
    const text = queryToSend || inputQuery;
    if (!text.trim() || isLoading) return;

    // Add User Message
    const userMsg = { id: Date.now(), sender: 'user', text };
    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setIsLoading(true);

    // Simulate Intelligence Processing
    setTimeout(() => {
      let matchedData = null;
      const lower = text.toLowerCase();

      if (lower.includes('water') || lower.includes('10500')) {
        matchedData = KNOWLEDGE_RESPONSES.water;
      } else if (lower.includes('isi') || lower.includes('consumer') || lower.includes('mark') || lower.includes('cml')) {
        matchedData = KNOWLEDGE_RESPONSES.consumer;
      } else if (lower.includes('certif') || lower.includes('process')) {
        matchedData = KNOWLEDGE_RESPONSES.certification;
      } else if (lower.includes('toy') || lower.includes('9873') || lower.includes('safety')) {
        matchedData = KNOWLEDGE_RESPONSES.toy;
      } else {
        matchedData = {
          answer: `Regarding your query "${text}": Jagruk Swadesh intelligence indexes official Bureau of Indian Standards documentation to provide source-backed insights. For complete standards verification, ISI licensing, and testing procedures, you can cross-reference official IS codes or submit specific standard numbers.`,
          sources: [
            "Bureau of Indian Standards Official Gazette & Rules",
            "Jagruk Swadesh Indian Standards Intelligence Engine"
          ]
        };
      }

      const botMsg = {
        id: Date.now() + 1,
        sender: 'bot',
        answer: matchedData.answer,
        sources: matchedData.sources,
      };

      setMessages((prev) => [...prev, botMsg]);
      setIsLoading(false);
    }, 1100);
  };

  const handleNewChat = () => {
    setMessages([]);
    setInputQuery('');
    setIsLoading(false);
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
        {/* Backdrop Overlay */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="fixed inset-0 bg-nature-950/85 backdrop-blur-md"
        />

        {/* Liquid Glass Modal Container */}
        <motion.div
          initial={{ opacity: 0, scale: 0.94, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.94, y: 20 }}
          transition={{ type: "spring", duration: 0.45, bounce: 0.15 }}
          className="relative w-full max-w-3xl h-[85vh] sm:h-[80vh] flex flex-col liquid-glass-panel border-saffron/40 z-10 shadow-2xl overflow-hidden"
        >
          
          {/* HEADER BAR */}
          <div className="px-5 py-4 border-b border-white/15 flex items-center justify-between bg-nature-950/70 backdrop-blur-xl shrink-0">
            <div className="flex items-center space-x-3">
              <Logo size="sm" showText={false} />
              <div>
                <div className="flex items-center space-x-2">
                  <h3 className="text-base sm:text-lg font-black text-white leading-none">
                    Jagruk Swadesh Assistant
                  </h3>
                  <span className="px-2 py-0.5 rounded-full bg-saffron/20 border border-saffron/40 text-[10px] font-extrabold text-saffron uppercase tracking-wider">
                    BIS Intelligence
                  </span>
                </div>
                <p className="text-xs text-ivory-muted font-medium mt-0.5">
                  Ask about Indian Standards, certification, testing & consumer guidance
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              {messages.length > 0 && (
                <button
                  onClick={handleNewChat}
                  className="px-3 py-1.5 rounded-full text-xs font-bold text-ivory-dim hover:text-white bg-white/10 hover:bg-white/20 border border-white/15 transition-all flex items-center space-x-1.5"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">New Chat</span>
                </button>
              )}
              <button
                onClick={onClose}
                className="p-2 rounded-full text-ivory hover:text-white hover:bg-white/15 transition-colors"
                aria-label="Close Assistant"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* MAIN MESSAGES / CONVERSATION AREA */}
          <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
            
            {/* EMPTY STATE — SUGGESTED QUESTIONS */}
            {messages.length === 0 && (
              <div className="h-full flex flex-col items-center justify-center text-center max-w-lg mx-auto py-8 space-y-6">
                <div className="w-16 h-16 rounded-2xl bg-amber-400/20 border border-amber-400/50 flex items-center justify-center text-amber-300 shadow-lg">
                  <Sparkles className="w-8 h-8" />
                </div>

                <div className="space-y-2">
                  <h4 className="text-xl sm:text-2xl font-bold text-white">
                    Ask about Indian Standards
                  </h4>
                  <p className="text-xs sm:text-sm text-ivory-muted font-medium leading-relaxed">
                    Get clear, source-backed answers for BIS certification, product testing limits, and compliance norms.
                  </p>
                </div>

                <div className="w-full space-y-2.5 pt-2">
                  <span className="text-xs font-semibold uppercase tracking-wider text-saffron block text-left pl-1">
                    Suggested Questions
                  </span>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                    {SUGGESTED_QUESTIONS.map((item, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleSend(item.q)}
                        className="p-3.5 rounded-xl bg-nature-950/80 hover:bg-nature-900 border border-white/20 hover:border-amber-400/60 text-left transition-all group flex flex-col justify-between space-y-2"
                      >
                        <span className="text-xs font-semibold text-white group-hover:text-amber-300 transition-colors leading-snug">
                          "{item.q}"
                        </span>
                        <div className="flex items-center justify-between text-[10px] text-ivory-dim font-semibold">
                          <span className="text-saffron">{item.category}</span>
                          <ArrowRight className="w-3.5 h-3.5 transform group-hover:translate-x-1 transition-transform text-amber-300" />
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* CONVERSATION HISTORY */}
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className={`flex gap-3.5 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {msg.sender === 'bot' && (
                  <div className="w-8 h-8 rounded-xl bg-saffron/25 border border-saffron/50 flex items-center justify-center text-saffron-light shrink-0 mt-1 shadow-md">
                    <Bot className="w-4 h-4" />
                  </div>
                )}

                <div className={`max-w-[85%] sm:max-w-[78%] rounded-2xl p-4 sm:p-5 space-y-3 ${
                  msg.sender === 'user'
                    ? 'bg-gradient-to-r from-saffron/30 to-amber-500/30 border border-saffron/50 text-white shadow-md'
                    : 'bg-nature-950/85 border border-white/20 text-white shadow-lg backdrop-blur-xl'
                }`}>
                  {msg.sender === 'user' ? (
                    <p className="text-sm font-semibold leading-relaxed text-white">
                      {msg.text}
                    </p>
                  ) : (
                    <div className="space-y-4 text-xs sm:text-sm font-medium">
                      
                      {/* ANSWER AREA */}
                      <div className="space-y-1.5">
                        <span className="text-[11px] font-black uppercase tracking-wider text-saffron block">
                          Answer
                        </span>
                        <p className="text-ivory leading-relaxed font-semibold">
                          {msg.answer}
                        </p>
                      </div>

                      {/* SOURCE-BACKED RESPONSE AREA */}
                      {msg.sources && msg.sources.length > 0 && (
                        <div className="pt-3 border-t border-white/15 space-y-2">
                          <div className="flex items-center space-x-1.5 text-xs font-extrabold text-amber-300">
                            <BookOpen className="w-3.5 h-3.5" />
                            <span>Sources</span>
                          </div>
                          <ul className="space-y-1.5 pl-1">
                            {msg.sources.map((src, i) => (
                              <li key={i} className="text-xs text-ivory-dim font-medium flex items-start space-x-2">
                                <span className="text-saffron font-bold">•</span>
                                <span>{src}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                    </div>
                  )}
                </div>

                {msg.sender === 'user' && (
                  <div className="w-8 h-8 rounded-xl bg-white/15 border border-white/30 flex items-center justify-center text-white shrink-0 mt-1 shadow-md">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </motion.div>
            ))}

            {/* LOADING STATE / TYPING INDICATOR */}
            {isLoading && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center space-x-3 text-ivory-dim"
              >
                <div className="w-8 h-8 rounded-xl bg-saffron/25 border border-saffron/50 flex items-center justify-center text-saffron-light shrink-0">
                  <Bot className="w-4 h-4 animate-pulse" />
                </div>
                <div className="px-4 py-3 rounded-2xl bg-nature-950/80 border border-white/20 flex items-center space-x-2 text-xs font-bold text-saffron">
                  <span className="w-2 h-2 rounded-full bg-saffron animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 rounded-full bg-saffron animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 rounded-full bg-saffron animate-bounce" style={{ animationDelay: '300ms' }} />
                  <span className="pl-1">Searching BIS Knowledge Base...</span>
                </div>
              </motion.div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* INPUT FORM FOOTER */}
          <div className="p-4 border-t border-white/15 bg-nature-950/80 backdrop-blur-xl shrink-0">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
              className="flex items-center space-x-3"
            >
              <input
                type="text"
                value={inputQuery}
                onChange={(e) => setInputQuery(e.target.value)}
                placeholder="Type your question about Indian Standards, BIS certification..."
                className="liquid-input flex-1 text-sm font-semibold placeholder:text-ivory-dim/60"
              />
              <button
                type="submit"
                disabled={!inputQuery.trim() || isLoading}
                className={`btn-saffron-liquid px-5 py-3 text-sm flex items-center space-x-2 shrink-0 ${
                  !inputQuery.trim() || isLoading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
              >
                <span>Send</span>
                <Send className="w-4 h-4" />
              </button>
            </form>
            <div className="flex items-center justify-between px-1 pt-2 text-[10px] text-ivory-dim font-semibold">
              <span className="flex items-center space-x-1">
                <ShieldCheck className="w-3 h-3 text-saffron" />
                <span>Verified Bureau of Indian Standards Context</span>
              </span>
              <span>Jagruk Swadesh Assistant</span>
            </div>
          </div>

        </motion.div>
      </div>
    </AnimatePresence>
  );
}

