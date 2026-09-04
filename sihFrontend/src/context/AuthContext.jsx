import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const AuthContext = createContext(null);

// All /api/* requests are proxied by Vite → Express (port 5000)
// so we just use a relative base URL — no hardcoded ports in the browser bundle.
const API_URL = '/api';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('js_token'));
  const [loading, setLoading] = useState(true); // true while we check for an existing session
  const [pendingChatbotAccess, setPendingChatbotAccess] = useState(false);

  // On first load, if a token was saved from a previous visit, validate it
  // against the API and restore the session instead of forcing a re-login.
  useEffect(() => {
    async function restoreSession() {
      if (!token) {
        setLoading(false);
        return;
      }
      try {
        const res = await fetch(`${API_URL}/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error('Session expired');
        const data = await res.json();
        setUser(data.user);
      } catch (err) {
        localStorage.removeItem('js_token');
        setToken(null);
        setUser(null);
      } finally {
        setLoading(false);
      }
    }
    restoreSession();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const login = useCallback(async (email, password) => {
    try {
      const res = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();

      if (!res.ok) {
        return { success: false, error: data.message || 'Invalid email or password' };
      }

      localStorage.setItem('js_token', data.token);
      setToken(data.token);
      setUser(data.user);
      return { success: true };
    } catch (err) {
      return { success: false, error: 'Could not reach the server. Please try again.' };
    }
  }, []);

  const signup = useCallback(async (fullName, email, password) => {
    try {
      const res = await fetch(`${API_URL}/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fullName, email, password }),
      });
      const data = await res.json();

      if (!res.ok) {
        return { success: false, error: data.message || 'Could not create account' };
      }

      // We deliberately do NOT log the user in here — SignUp.jsx redirects to
      // /login after a successful signup, matching the existing UX.
      return { success: true };
    } catch (err) {
      return { success: false, error: 'Could not reach the server. Please try again.' };
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('js_token');
    setToken(null);
    setUser(null);
  }, []);

  const value = {
    user,
    isAuthenticated: !!user,
    loading,
    login,
    signup,
    logout,
    pendingChatbotAccess,
    setPendingChatbotAccess,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within an AuthProvider');
  return ctx;
}
