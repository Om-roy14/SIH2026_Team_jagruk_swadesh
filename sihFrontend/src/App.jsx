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


/* =========================================================
   Scroll To Top
========================================================= */

function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  }, [pathname]);

  return null;
}


/* =========================================================
   Main Layout
========================================================= */

function MainLayout() {
  const [isChatbotModalOpen, setIsChatbotModalOpen] = useState(false);

  const {
    isAuthenticated,
    pendingChatbotAccess,
    setPendingChatbotAccess,
  } = useAuth();

  const navigate = useNavigate();
  const { pathname } = useLocation();

  /*
   * Chatbot uses a full-screen layout.
   * Other pages retain the normal Navbar/Footer structure.
   */
  const isChatbotPage = pathname === '/chatbot';


  /* =======================================================
     Pending Chatbot Access
  ======================================================= */

  useEffect(() => {
    if (isAuthenticated && pendingChatbotAccess) {
      navigate('/chatbot');
      setPendingChatbotAccess(false);
    }
  }, [
    isAuthenticated,
    pendingChatbotAccess,
    navigate,
    setPendingChatbotAccess,
  ]);


  /* =======================================================
     Open Chatbot
  ======================================================= */

  const handleOpenChatbotModal = () => {
    if (isAuthenticated) {
      navigate('/chatbot');
    } else {
      setPendingChatbotAccess(true);
      navigate('/login');
    }
  };


  /* =======================================================
     Close Chatbot Modal
  ======================================================= */

  const handleCloseChatbotModal = () => {
    setIsChatbotModalOpen(false);
  };


  /* =======================================================
     Application Layout
  ======================================================= */

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

      {/* Background */}
      <div
        className="bg-nature-environment"
        aria-hidden="true"
      />

      <div
        className="bg-nature-overlay"
        aria-hidden="true"
      />


      {/* Global Cursor Effect */}
      <CursorGlow />


      {/* Scroll Management */}
      <ScrollToTop />


      {/* ===================================================
          Navbar
      =================================================== */}

      <Navbar
        onOpenChatbotModal={handleOpenChatbotModal}
      />


      {/* ===================================================
          Main Application Content
      =================================================== */}

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

          {/* Home */}
          <Route
            path="/"
            element={
              <Home
                onOpenChatbotModal={handleOpenChatbotModal}
              />
            }
          />


          {/* Explore */}
          <Route
            path="/explore"
            element={
              <Explore
                onOpenChatbotModal={handleOpenChatbotModal}
              />
            }
          />


          {/* About */}
          <Route
            path="/about"
            element={
              <About
                onOpenChatbotModal={handleOpenChatbotModal}
              />
            }
          />


          {/* =================================================
              AI Chatbot
          ================================================= */}

          <Route
            path="/chatbot"
            element={<Chatbot />}
          />


          {/* =================================================
              Product QR Verification
              
              Flow:
              Chatbot
                 ↓
              Scan Product
                 ↓
              /product-details
                 ↓
              QR Scanner
                 ↓
              Product Details
          ================================================= */}

          <Route
            path="/product-details"
            element={<ProductDetails />}
          />


          {/* Login */}
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


          {/* Signup */}
          <Route
            path="/signup"
            element={<SignUp />}
          />


          {/* Privacy Policy */}
          <Route
            path="/privacy"
            element={<PrivacyPolicy />}
          />

        </Routes>
      </main>


      {/* ===================================================
          Footer
          
          Hidden on chatbot because chatbot occupies the
          complete viewport.
      =================================================== */}

      {!isChatbotPage && (
        <Footer
          onOpenChatbotModal={handleOpenChatbotModal}
        />
      )}


      {/* ===================================================
          Chatbot Integration Modal
      =================================================== */}

      {isAuthenticated && (
        <ChatbotIntegrationModal
          isOpen={isChatbotModalOpen}
          onClose={handleCloseChatbotModal}
        />
      )}

    </div>
  );
}


/* =========================================================
   Application Root
========================================================= */

export default function App() {
  return (
    <AuthProvider>
      <MainLayout />
    </AuthProvider>
  );
}