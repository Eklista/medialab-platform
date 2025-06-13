// frontend/src/App.tsx (actualizado para integrar CMS como landing)
import { AuthRouter } from './modules/auth/AuthRouter';
import { CMSRouter } from './modules/cmsFrontend/CMSRouter';
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

  // Determinar qué mostrar basado en la URL
  const currentPath = window.location.pathname;
  
  // Si está en rutas de auth, mostrar AuthRouter
  if (currentPath.startsWith('/auth') || currentPath === '/login') {
    console.log('App - Rendering AuthRouter');
    return (
      <div className="min-h-screen bg-slate-50">
        <AuthRouter />
      </div>
    );
  }

  // Por defecto, mostrar CMS Frontend como landing
  console.log('App - Rendering CMS Landing');
  return <CMSRouter />;
}

export default App;