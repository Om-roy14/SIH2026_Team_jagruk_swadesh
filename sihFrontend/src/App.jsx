import React, { useState, useEffect } from 'react';
import { Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ChatbotIntegrationModal from './components/ChatbotIntegrationModal';
import CursorGlow from './components/CursorGlow';
import { AuthProvider, useAuth } from './context/AuthContext';

import Home from './pages/Home';
import Explore from './pages/Explore';
import About from './pages/About';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import PrivacyPolicy from './pages/PrivacyPolicy';
import Chatbot from './pages/Chatbot';

// Scroll to top component on route change
function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
}

function MainLayout() {
  const [isChatbotModalOpen, setIsChatbotModalOpen] = useState(false);
  const { isAuthenticated, pendingChatbotAccess, setPendingChatbotAccess } = useAuth();
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const isChatbotPage = pathname === '/chatbot';

  // If user just logged in after trying to access chatbot, open modal automatically or navigate to chatbot
  useEffect(() => {
    if (isAuthenticated && pendingChatbotAccess) {
      navigate('/chatbot');
      setPendingChatbotAccess(false);
    }
  }, [isAuthenticated, pendingChatbotAccess, setPendingChatbotAccess, navigate]);

  const handleOpenChatbotModal = () => {
    if (isAuthenticated) {
      navigate('/chatbot');
    } else {
      setPendingChatbotAccess(true);
      navigate('/login');
    }
  };

  const handleCloseChatbotModal = () => {
    setIsChatbotModalOpen(false);
  };

  return (
    <div className={`relative flex flex-col overflow-x-hidden ${isChatbotPage ? 'h-screen overflow-hidden' : 'min-h-screen justify-between'}`}>
      
      {/* 1. PRIMARY GREEN ATMOSPHERIC BACKGROUND LAYER */}
      <div className="bg-nature-environment" aria-hidden="true" />
      <div className="bg-nature-overlay" aria-hidden="true" />

      {/* 2. SUBTLE CURSOR FOLLOWING LIQUID AURA */}
      <CursorGlow />

      {/* Scroll Restorer */}
      <ScrollToTop />

      {/* 3. NAVBAR */}
      <Navbar onOpenChatbotModal={handleOpenChatbotModal} />

      {/* 4. MAIN ROUTED CONTENT */}
      <main className={`flex-grow ${isChatbotPage ? 'flex flex-col min-h-0' : ''}`}>
        <Routes>
          <Route path="/" element={<Home onOpenChatbotModal={handleOpenChatbotModal} />} />
          <Route path="/explore" element={<Explore onOpenChatbotModal={handleOpenChatbotModal} />} />
          <Route path="/about" element={<About onOpenChatbotModal={handleOpenChatbotModal} />} />
          <Route path="/chatbot" element={<Chatbot />} />
          <Route path="/login" element={<Login onOpenChatbotModal={() => navigate('/chatbot')} />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/privacy" element={<PrivacyPolicy />} />
        </Routes>
      </main>

      {/* 5. FOOTER */}
      {!isChatbotPage && <Footer onOpenChatbotModal={handleOpenChatbotModal} />}

      {/* 6. CHATBOT INTEGRATION CTA MODAL (PROTECTED) */}
      {isAuthenticated && (
        <ChatbotIntegrationModal
          isOpen={isChatbotModalOpen}
          onClose={handleCloseChatbotModal}
        />
      )}
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <MainLayout />
    </AuthProvider>
  );
}
