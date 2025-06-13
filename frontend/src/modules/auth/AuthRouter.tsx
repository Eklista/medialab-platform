// modules/auth/AuthRouter.tsx
import React from 'react';
import { useAuth } from '../../shared/context/AuthContext';
import { LoadingScreen } from '../../shared/components/LoadingScreen';
import { LoginPage } from './pages/LoginPage';
import { TwoFactorPage } from './pages/TwoFactorPage';
import { RecoveryPage } from './pages/RecoveryPage';
import { AuthNavigationProvider, useAuthNavigation } from './context/AuthNavigationContext';

const AuthContent: React.FC = () => {
  const { is_authenticated, requires_2fa, is_loading } = useAuth();
  const { currentRoute, navigateTo2FA } = useAuthNavigation();

  console.log('AuthContent - Render state:', { is_authenticated, requires_2fa, is_loading, currentRoute });

  React.useEffect(() => {
    if (requires_2fa) {
      navigateTo2FA();
    }
  }, [requires_2fa, navigateTo2FA]);

  if (is_loading) {
    console.log('AuthContent - Rendering LoadingScreen');
    return <LoadingScreen />;
  }

  // Si ya está autenticado, no renderizar nada (App.tsx manejará el dashboard)
  if (is_authenticated) {
    console.log('AuthContent - User authenticated, returning null');
    return null;
  }

  const renderRoute = () => {
    switch (currentRoute) {
      case 'login':
        return <LoginPage />;
      case '2fa':
        return <TwoFactorPage />;
      case 'recovery':
        return <RecoveryPage />;
      default:
        return <LoginPage />;
    }
  };

  console.log('AuthContent - Rendering route:', currentRoute);
  return <>{renderRoute()}</>;
};

export const AuthRouter: React.FC = () => {
  return (
    <AuthNavigationProvider>
      <AuthContent />
    </AuthNavigationProvider>
  );
};