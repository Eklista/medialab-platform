// src/App.tsx
import React from 'react';
import { AuthRouter } from './modules/auth/AuthRouter';
import { DashboardHome } from './modules/dashboardHome/DashboardHome';
import { useAuth } from './shared/context/AuthContext';
import { LoadingScreen } from './shared/components/LoadingScreen';

function App() {
  const { user, is_authenticated, is_loading, logout } = useAuth();

  console.log('App - Render with auth state:', {
    isAuthenticated: is_authenticated,
    isLoading: is_loading,
    hasUser: !!user
  });

  // Mostrar loading mientras se valida la sesión
  if (is_loading) {
    console.log('App - Rendering LoadingScreen');
    return <LoadingScreen />;
  }

  // Si está autenticado, mostrar dashboard
  if (is_authenticated && user) {
    console.log('App - Rendering Dashboard for user:', user.email);
    return (
      <DashboardHome 
        user={user}
        onLogout={logout}
      />
    );
  }

  // Si no está autenticado, mostrar auth
  console.log('App - Rendering AuthRouter');
  return (
    <div className="min-h-screen bg-slate-50">
      <AuthRouter />
    </div>
  );
}

export default App;