// modules/auth/pages/LoginPage.tsx
import React from 'react';
import { AuthLayout } from '../components/AuthLayout';
import { LoginCard } from '../components/LoginCard';
import { useAuth } from '../../../shared/hooks/useAuth';

export const LoginPage: React.FC = () => {
  const { login, isLoading, error, clearError } = useAuth();

  const handleLogin = async (data: { identifier: string; password: string; remember_me: boolean }) => {
    clearError();
    
    await login({
      ...data,
      device_name: getDeviceName()
    });
  };

  const handleGoogleLogin = () => {
    console.log('Google login - Por implementar');
  };

  const getDeviceName = (): string => {
    const userAgent = navigator.userAgent;
    
    if (/iPhone/i.test(userAgent)) return 'iPhone';
    if (/iPad/i.test(userAgent)) return 'iPad';
    if (/Android/i.test(userAgent)) return 'Android';
    if (/Mac/i.test(userAgent)) return 'Mac';
    if (/Windows/i.test(userAgent)) return 'Windows PC';
    if (/Linux/i.test(userAgent)) return 'Linux PC';
    
    return 'Dispositivo Desconocido';
  };

  return (
    <AuthLayout
      title="Iniciar Sesión"
      subtitle="Accede a tu cuenta de MediaLab"
      showLogo={true}
    >
      <LoginCard
        onSubmit={handleLogin}
        onGoogleLogin={handleGoogleLogin}
        isLoading={isLoading}
        error={error || undefined}
      />
    </AuthLayout>
  );
};