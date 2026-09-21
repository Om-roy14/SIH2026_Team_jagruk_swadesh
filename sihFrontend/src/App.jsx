import React, { useState, useEffect } from 'react';
import {
  Routes,
  Route,
  useLocation,
  useNavigate,
} from 'react-router-dom';

import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ChatbotIntegrationModal from './components/ChatbotIntegrationModal';
import CursorGlow from './components/CursorGlow';
import ProductDetails from './components/ProductDetails';

import { AuthProvider, useAuth } from './context/AuthContext';

import Home from './pages/Home';
import Explore from './pages/Explore';
import About from './pages/About';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import PrivacyPolicy from './pages/PrivacyPolicy';
import Chatbot from './pages/Chatbot';


// ============================================================
// SCROLL TO TOP
// ============================================================

function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
}


// ============================================================
// MAIN LAYOUT
// ============================================================

function MainLayout() {
  const [isChatbotModalOpen, setIsChatbotModalOpen] = useState(false);

  const {
    isAuthenticated,
    pendingChatbotAccess,
    setPendingChatbotAccess,
  } = useAuth();

  const navigate = useNavigate();
  const { pathname } = useLocation();

  const isChatbotPage = pathname === '/chatbot';


  // ==========================================================
  // HANDLE PENDING CHATBOT ACCESS
  // ==========================================================

  useEffect(() => {
    if (isAuthenticated && pendingChatbotAccess) {
      navigate('/chatbot');
      setPendingChatbotAccess(false);
    }
  }, [
    isAuthenticated,
    pendingChatbotAccess,
    setPendingChatbotAccess,
    navigate,
  ]);


  // ==========================================================
  // OPEN CHATBOT
  // ==========================================================

  const handleOpenChatbotModal = () => {
    if (isAuthenticated) {
      navigate('/chatbot');
    } else {
      setPendingChatbotAccess(true);
      navigate('/login');
    }
  };


  // ==========================================================
  // CLOSE CHATBOT MODAL
  // ==========================================================

  const handleCloseChatbotModal = () => {
    setIsChatbotModalOpen(false);
  };


  // ==========================================================
  // MAIN LAYOUT
  // ==========================================================

  return (
    <div
      className={`
        relative
        flex
        flex-col
        overflow-x-hidden
        ${
          isChatbotPage
            ? 'h-screen overflow-hidden'
            : 'min-h-screen justify-between'
        }
      `}
    >

      {/* ======================================================
          1. PRIMARY GREEN ATMOSPHERIC BACKGROUND
      ====================================================== */}

      <div
        className="bg-nature-environment"
        aria-hidden="true"
      />

      <div
        className="bg-nature-overlay"
        aria-hidden="true"
      />


      {/* ======================================================
          2. CURSOR FOLLOWING LIQUID AURA
      ====================================================== */}

      <CursorGlow />


      {/* ======================================================
          3. SCROLL RESTORER
      ====================================================== */}

      <ScrollToTop />


      {/* ======================================================
          4. NAVBAR
      ====================================================== */}

      <Navbar
        onOpenChatbotModal={handleOpenChatbotModal}
      />


      {/* ======================================================
          5. MAIN ROUTED CONTENT
      ====================================================== */}

      <main
        className={`
          flex-grow
          ${
            isChatbotPage
              ? 'flex flex-col min-h-0'
              : ''
          }
        `}
      >

        <Routes>

          {/* ==================================================
              HOME
          ================================================== */}

          <Route
            path="/"
            element={
              <Home
                onOpenChatbotModal={handleOpenChatbotModal}
              />
            }
          />


          {/* ==================================================
              EXPLORE
          ================================================== */}

          <Route
            path="/explore"
            element={
              <Explore
                onOpenChatbotModal={handleOpenChatbotModal}
              />
            }
          />


          {/* ==================================================
              ABOUT
          ================================================== */}

          <Route
            path="/about"
            element={
              <About
                onOpenChatbotModal={handleOpenChatbotModal}
              />
            }
          />


          {/* ==================================================
              CHATBOT
          ================================================== */}

          <Route
            path="/chatbot"
            element={<Chatbot />}
          />


          {/* ==================================================
              PRODUCT DETAILS / QR VERIFICATION
              
              ProductDetails.jsx is located at:
              
              src/components/ProductDetails.jsx
          ================================================== */}

          <Route
            path="/product-details"
            element={<ProductDetails />}
          />


          {/* ==================================================
              LOGIN
          ================================================== */}

          <Route
            path="/login"
            element={
              <Login
                onOpenChatbotModal={() =>
                  navigate('/chatbot')
                }
              />
            }
          />


          {/* ==================================================
              SIGN UP
          ================================================== */}

          <Route
            path="/signup"
            element={<SignUp />}
          />


          {/* ==================================================
              PRIVACY POLICY
          ================================================== */}

          <Route
            path="/privacy"
            element={<PrivacyPolicy />}
          />

        </Routes>

      </main>


      {/* ======================================================
          6. FOOTER
          
          Footer is hidden on the chatbot page because the
          chatbot uses the full screen.
      ====================================================== */}

      {!isChatbotPage && (
        <Footer
          onOpenChatbotModal={handleOpenChatbotModal}
        />
      )}


      {/* ======================================================
          7. CHATBOT INTEGRATION MODAL
          
          Only authenticated users can access this modal.
      ====================================================== */}

      {isAuthenticated && (
        <ChatbotIntegrationModal
          isOpen={isChatbotModalOpen}
          onClose={handleCloseChatbotModal}
        />
      )}

    </div>
  );
}


// ============================================================
// APP
// ============================================================

export default function App() {
  return (
    <AuthProvider>
      <MainLayout />
    </AuthProvider>
  );
}