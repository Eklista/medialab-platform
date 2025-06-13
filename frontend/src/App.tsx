// src/App.tsx
import { useState } from 'react';
import { AuthRouter } from './modules/auth/AuthRouter';
import { DashboardHome } from './modules/dashboardHome/DashboardHome';
import { useAuth } from './shared/hooks/useAuth';

function App() {
  const { user, logout } = useAuth();
  const [showDashboard, setShowDashboard] = useState(false);

  const handleAuthenticated = () => {
    setShowDashboard(true);
  };

  const handleLogout = async () => {
    await logout();
    setShowDashboard(false);
  };

  if (showDashboard && user) {
    return (
      <DashboardHome 
        user={user}
        onLogout={handleLogout}
      />
    );
  }

  return (
    <div className="min-h-screen bg-zinc-950">
      <AuthRouter onAuthenticated={handleAuthenticated} />
    </div>
  );
}

export default App;