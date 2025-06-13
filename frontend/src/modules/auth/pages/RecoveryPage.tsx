// modules/auth/pages/RecoveryPage.tsx
import React from 'react';
import { AuthLayout } from '../components/AuthLayout';
import { RecoveryCard } from '../components/RecoveryCard';

export const RecoveryPage: React.FC = () => {
  const handleRecovery = async (email: string) => {
    console.log('Solicitar recuperación para:', email);
  };

  return (
    <AuthLayout
      title="Recuperar Contraseña"
      subtitle="Te enviaremos un enlace para restablecer tu contraseña"
      showLogo={true}
    >
      <RecoveryCard
        onSubmit={handleRecovery}
        isLoading={false}
      />
    </AuthLayout>
  );
};