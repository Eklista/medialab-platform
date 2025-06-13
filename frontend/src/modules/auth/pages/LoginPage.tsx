// modules/auth/pages/LoginPage.tsx
import React from 'react';
import { AuthLayout } from '../components/AuthLayout';
import { LoginCard } from '../components/LoginCard';
import { useAuth } from '../../../shared/context/AuthContext';

export const LoginPage: React.FC = () => {
  const { login, is_loading, error, clearError, is_authenticated } = useAuth();

  // Debug: log cuando cambie isAuthenticated
  React.useEffect(() => {
    console.log('LoginPage - is_authenticated changed:', is_authenticated);
  }, [is_authenticated]);

  const handleLogin = async (data: { identifier: string; password: string; remember_me: boolean }) => {
    console.log('LoginPage - Attempting login with:', data.identifier);
    clearError();
    
    try {
      const result = await login({
        ...data,
        device_name: getDeviceName()
      });
      
      console.log('LoginPage - Login result:', result);
      
      // El estado se debería actualizar automáticamente en useAuth
      // No necesitamos hacer nada más aquí
      
    } catch (error) {
      console.error('LoginPage - Login error:', error);
    }
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

  // Debug: Si ya está autenticado, no debería mostrar esta página
  if (is_authenticated) {
    console.log('LoginPage - User is authenticated, this page should not be visible');
  }

  return (
    <AuthLayout
      title="Iniciar Sesión"
      subtitle="Accede a tu cuenta de MediaLab"
      showLogo={true}
    >
      <LoginCard
        onSubmit={handleLogin}
        onGoogleLogin={handleGoogleLogin}
        isLoading={is_loading}
        error={error || undefined}
      />
    </AuthLayout>
  );
};