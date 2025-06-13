// src/App.tsx
import { useEffect, useState } from 'react';
import { AuthLayout } from './modules/auth/components/AuthLayout';
import { LoginCard } from './modules/auth/components/LoginCard';
import { TwoFactorCard } from './modules/auth/components/TwoFactorCard';
import { useAuth } from './shared/hooks/useAuth';
import { LoadingScreen } from './shared/components/LoadingScreen';
import { DashboardHome } from './modules/dashboardHome/DashboardHome';

type AppState = 'loading' | 'login' | '2fa' | 'dashboard';

function App() {
  const { 
    isAuthenticated, 
    requires2FA, 
    isLoading, 
    error, 
    login, 
    verify2FA, 
    clearError,
    user 
  } = useAuth();
  
  const [appState, setAppState] = useState<AppState>('loading');

  // Determinar estado de la app
  useEffect(() => {
    if (isLoading) {
      setAppState('loading');
    } else if (isAuthenticated) {
      setAppState('dashboard');
    } else if (requires2FA) {
      setAppState('2fa');
    } else {
      setAppState('login');
    }
  }, [isAuthenticated, requires2FA, isLoading]);

  // Handler para login
  const handleLogin = async (data: { identifier: string; password: string; remember_me: boolean }) => {
    clearError();
    
    const result = await login({
      ...data,
      device_name: getDeviceName()
    });

    if (result.success && !result.requires_2fa) {
      // Login exitoso, el estado se actualizará automáticamente
      console.log('Login exitoso');
    } else if (result.requires_2fa) {
      // Requiere 2FA, el estado se actualizará automáticamente
      console.log('Requiere 2FA');
    } else {
      // Error manejado por el hook
      console.error('Error en login:', result.error);
    }
  };

  // Handler para 2FA
  const handleTwoFactor = async (code: string) => {
    const result = await verify2FA(code);
    
    if (result.success) {
      console.log('2FA exitoso');
    } else {
      console.error('Error en 2FA:', result.error);
    }
  };

  // Handler para Google Login (placeholder)
  const handleGoogleLogin = () => {
    console.log('Google login - Por implementar');
    // TODO: Implementar OAuth con Google
  };

  // Función helper para obtener nombre del dispositivo
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

  // Renderizado condicional basado en el estado
  const renderContent = () => {
    switch (appState) {
      case 'loading':
        return <LoadingScreen />;
        
      case 'login':
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
              error={error || undefined} // ← Fix: null to undefined
            />
          </AuthLayout>
        );
        
      case '2fa':
        return (
          <AuthLayout
            title="Verificación 2FA"
            subtitle="Ingresa el código de tu aplicación autenticadora"
            showLogo={false}
          >
            <TwoFactorCard
              onSubmit={handleTwoFactor}
              isLoading={isLoading}
              error={error || undefined} // ← Fix: null to undefined
              expiresIn={600}
            />
          </AuthLayout>
        );
        
      case 'dashboard':
        return (
          <DashboardHome 
            user={user}
            onLogout={() => window.location.reload()}
          />
        );
        
      default:
        return <LoadingScreen />;
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950">
      {renderContent()}
    </div>
  );
}

export default App;