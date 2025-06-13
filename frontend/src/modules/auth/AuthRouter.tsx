// modules/auth/AuthRouter.tsx
import React from 'react';
import { useAuth } from '../../shared/hooks/useAuth';
import { LoadingScreen } from '../../shared/components/LoadingScreen';
import { LoginPage } from './pages/LoginPage';
import { TwoFactorPage } from './pages/TwoFactorPage';
import { RecoveryPage } from './pages/RecoveryPage';
import { AuthNavigationProvider, useAuthNavigation } from './context/AuthNavigationContext';

interface AuthRouterProps {
  onAuthenticated: () => void;
}

const AuthContent: React.FC<AuthRouterProps> = ({ onAuthenticated }) => {
  const { isAuthenticated, requires2FA, isLoading } = useAuth();
  const { currentRoute, navigateTo2FA } = useAuthNavigation();

  React.useEffect(() => {
    if (isAuthenticated) {
      onAuthenticated();
    } else if (requires2FA) {
      navigateTo2FA();
    }
  }, [isAuthenticated, requires2FA, onAuthenticated, navigateTo2FA]);

  if (isLoading) {
    return <LoadingScreen />;
  }

  if (isAuthenticated) {
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

  return <>{renderRoute()}</>;
};

export const AuthRouter: React.FC<AuthRouterProps> = ({ onAuthenticated }) => {
  return (
    <AuthNavigationProvider>
      <AuthContent onAuthenticated={onAuthenticated} />
    </AuthNavigationProvider>
  );
};