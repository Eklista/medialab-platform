// modules/auth/pages/TwoFactorPage.tsx
import React from 'react';
import { AuthLayout } from '../components/AuthLayout';
import { TwoFactorCard } from '../components/TwoFactorCard';
import { useAuth } from '../../../shared/hooks/useAuth';

export const TwoFactorPage: React.FC = () => {
  const { verify2FA, isLoading, error } = useAuth();

  const handleTwoFactor = async (code: string) => {
    await verify2FA(code);
  };

  return (
    <AuthLayout
      title="Verificación 2FA"
      subtitle="Ingresa el código de tu aplicación autenticadora"
      showLogo={false}
    >
      <TwoFactorCard
        onSubmit={handleTwoFactor}
        isLoading={isLoading}
        error={error || undefined}
        expiresIn={600}
      />
    </AuthLayout>
  );
};