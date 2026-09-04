import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Mail, Lock, ArrowRight, CheckCircle2 } from 'lucide-react';
import PageTransition from '../components/PageTransition';
import Input from '../components/Input';
import Button from '../components/Button';
import Logo from '../components/Logo';
import { useAuth } from '../context/AuthContext';

export default function Login({ onOpenChatbotModal }) {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (errors[e.target.name]) {
      setErrors({ ...errors, [e.target.name]: '' });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = {};
    if (!formData.email.trim()) newErrors.email = 'Email address is required';
    else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = 'Please enter a valid email';

    if (!formData.password) newErrors.password = 'Password is required';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsSubmitting(true);
    const result = await login(formData.email, formData.password);
    setIsSubmitting(false);

    if (!result.success) {
      setErrors({ form: result.error });
      return;
    }

    setSubmitted(true);

    setTimeout(() => {
      navigate('/chatbot');
      if (onOpenChatbotModal) {
        onOpenChatbotModal();
      }
    }, 1200);
  };

  return (
    <PageTransition>
      <div className="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8 pt-24 pb-16">
        
        {/* Centered Translucent Auth Box */}
        <div className="w-full max-w-md liquid-glass-panel p-7 sm:p-9 space-y-7 border-white/15 relative">
          
          {/* Header with Logo */}
          <div className="text-center space-y-3">
            <div className="flex justify-center">
              <Logo size="md" />
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Welcome Back
            </h2>
            <p className="text-xs sm:text-sm text-ivory-muted font-normal">
              Access your Jagruk Swadesh account & saved queries.
            </p>
          </div>

          {submitted ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              className="p-6 rounded-xl bg-forest-dark/90 border border-emerald-400/40 text-center space-y-2.5"
            >
              <CheckCircle2 className="w-9 h-9 text-emerald-400 mx-auto" />
              <h3 className="text-base font-bold text-white">Login Successful</h3>
              <p className="text-xs text-ivory-muted font-normal">Redirecting you to AI Chatbot...</p>
            </motion.div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4.5">
              {errors.form && (
                <div className="px-4 py-2.5 rounded-lg bg-red-500/10 border border-red-400/40 text-xs text-red-300 font-semibold text-center">
                  {errors.form}
                </div>
              )}

              <Input
                label="Email Address"
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="name@example.com"
                icon={Mail}
                error={errors.email}
                required
              />

              <div className="space-y-1">
                <Input
                  label="Password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="••••••••"
                  icon={Lock}
                  error={errors.password}
                  isPassword={true}
                  showPassword={showPassword}
                  onTogglePassword={() => setShowPassword(!showPassword)}
                  required
                />
                
                <div className="flex justify-end pt-1">
                  <a
                    href="#forgot"
                    onClick={(e) => { e.preventDefault(); alert('Password reset link sent to your registered email.'); }}
                    className="text-xs text-emerald-300 hover:text-white transition-colors font-semibold"
                  >
                    Forgot Password?
                  </a>
                </div>
              </div>

              <Button
                type="submit"
                variant="primary"
                size="lg"
                icon={ArrowRight}
                className="w-full mt-2"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Logging in...' : 'Login'}
              </Button>
            </form>
          )}

          {/* Footer Link */}
          <div className="pt-4 border-t border-white/10 text-center text-xs text-ivory-muted font-normal">
            <span>Don't have an account? </span>
            <Link to="/signup" className="text-emerald-300 font-semibold hover:text-white transition-colors">
              Sign Up
            </Link>
          </div>

        </div>

      </div>
    </PageTransition>
  );
}
