import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { User, Mail, Lock, ArrowRight, CheckCircle2 } from 'lucide-react';
import PageTransition from '../components/PageTransition';
import Input from '../components/Input';
import Button from '../components/Button';
import Logo from '../components/Logo';
import { useAuth } from '../context/AuthContext';

export default function SignUp() {
  const navigate = useNavigate();
  const { signup } = useAuth();
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
    agreePrivacy: false,
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({ ...formData, [e.target.name]: value });
    if (errors[e.target.name]) {
      setErrors({ ...errors, [e.target.name]: '' });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = {};

    if (!formData.fullName.trim()) newErrors.fullName = 'Full Name is required';
    if (!formData.email.trim()) newErrors.email = 'Email address is required';
    else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = 'Please enter a valid email';

    if (!formData.password) newErrors.password = 'Password is required';
    else if (formData.password.length < 6) newErrors.password = 'Password must be at least 6 characters';

    if (formData.confirmPassword !== formData.password) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (!formData.agreePrivacy) {
      newErrors.agreePrivacy = 'You must acknowledge the Privacy Policy';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsSubmitting(true);
    const result = await signup(formData.fullName, formData.email, formData.password);
    setIsSubmitting(false);

    if (!result.success) {
      setErrors({ form: result.error });
      return;
    }

    // Do not auto-login after signup; redirect to login page
    setSubmitted(true);
    setTimeout(() => {
      navigate('/login');
    }, 1500);
  };

  return (
    <PageTransition>
      <div className="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8 pt-24 pb-16">
        
        {/* Centered Translucent Auth Box */}
        <div className="w-full max-w-lg liquid-glass-panel p-7 sm:p-9 space-y-7 border-white/15 relative">
          
          {/* Header with Logo */}
          <div className="text-center space-y-3">
            <div className="flex justify-center">
              <Logo size="md" />
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Create Your Account
            </h2>
            <p className="text-xs sm:text-sm text-ivory-muted font-normal">
              Join Jagruk Swadesh to discover & understand Indian Standards.
            </p>
          </div>

          {submitted ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              className="p-6 rounded-xl bg-forest-dark/90 border border-emerald-400/40 text-center space-y-2.5"
            >
              <CheckCircle2 className="w-9 h-9 text-emerald-400 mx-auto" />
              <h3 className="text-base font-bold text-white">Account Created Successfully</h3>
              <p className="text-xs text-ivory-muted font-normal">Redirecting you to login page...</p>
            </motion.div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              {errors.form && (
                <div className="px-4 py-2.5 rounded-lg bg-red-500/10 border border-red-400/40 text-xs text-red-300 font-semibold text-center">
                  {errors.form}
                </div>
              )}

              <Input
                label="Full Name"
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                placeholder="Rajesh Kumar"
                icon={User}
                error={errors.fullName}
                required
              />

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

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
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

                <Input
                  label="Confirm Password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  placeholder="••••••••"
                  icon={Lock}
                  error={errors.confirmPassword}
                  isPassword={true}
                  showPassword={showConfirmPassword}
                  onTogglePassword={() => setShowConfirmPassword(!showConfirmPassword)}
                  required
                />
              </div>

              {/* Privacy Policy Checkbox */}
              <div className="space-y-1 pt-1">
                <label className="flex items-start space-x-2.5 cursor-pointer">
                  <input
                    type="checkbox"
                    name="agreePrivacy"
                    checked={formData.agreePrivacy}
                    onChange={handleChange}
                    className="mt-0.5 rounded bg-forest-dark border-white/20 text-emerald-400 focus:ring-emerald-400 focus:ring-offset-0"
                  />
                  <span className="text-xs text-ivory-muted font-normal leading-tight">
                    I acknowledge that I have read and agree to the{' '}
                    <Link to="/privacy" className="text-emerald-300 font-semibold hover:underline">
                      Privacy Policy
                    </Link>.
                  </span>
                </label>
                {errors.agreePrivacy && (
                  <p className="text-xs text-red-400 font-bold pl-1">{errors.agreePrivacy}</p>
                )}
              </div>

              <Button
                type="submit"
                variant="primary"
                size="lg"
                icon={ArrowRight}
                className="w-full mt-2"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Creating account...' : 'Create Account'}
              </Button>
            </form>
          )}

          {/* Footer Link */}
          <div className="pt-4 border-t border-white/10 text-center text-xs text-ivory-muted font-normal">
            <span>Already have an account? </span>
            <Link to="/login" className="text-emerald-300 font-semibold hover:text-white transition-colors">
              Login
            </Link>
          </div>

        </div>

      </div>
    </PageTransition>
  );
}
