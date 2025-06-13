// modules/auth/context/AuthNavigationContext.tsx
import React, { createContext, useContext, useState } from 'react';

type AuthRoute = 'login' | '2fa' | 'recovery';

interface AuthNavigationContextType {
  currentRoute: AuthRoute;
  navigateToLogin: () => void;
  navigateToRecovery: () => void;
  navigateTo2FA: () => void;
}

const AuthNavigationContext = createContext<AuthNavigationContextType | undefined>(undefined);

interface AuthNavigationProviderProps {
  children: React.ReactNode;
  initialRoute?: AuthRoute;
}

export const AuthNavigationProvider: React.FC<AuthNavigationProviderProps> = ({
  children,
  initialRoute = 'login'
}) => {
  const [currentRoute, setCurrentRoute] = useState<AuthRoute>(initialRoute);

  const navigateToLogin = () => setCurrentRoute('login');
  const navigateToRecovery = () => setCurrentRoute('recovery');
  const navigateTo2FA = () => setCurrentRoute('2fa');

  return (
    <AuthNavigationContext.Provider
      value={{
        currentRoute,
        navigateToLogin,
        navigateToRecovery,
        navigateTo2FA,
      }}
    >
      {children}
    </AuthNavigationContext.Provider>
  );
};

export const useAuthNavigation = () => {
  const context = useContext(AuthNavigationContext);
  if (context === undefined) {
    throw new Error('useAuthNavigation must be used within an AuthNavigationProvider');
  }
  return context;
};