// modules/auth/components/RecoveryCard.tsx
import React from 'react';
import { useForm, type SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { EmailInput } from '../ui/inputs/EmailInput';
import { LoginButton } from '../ui/buttons/LoginButton';
import { useAuthNavigation } from '../context/AuthNavigationContext';

const recoverySchema = z.object({
  email: z.string().email('Ingresa un correo válido'),
});

type RecoveryFormData = z.infer<typeof recoverySchema>;

interface RecoveryCardProps {
  onSubmit: (email: string) => Promise<void>;
  isLoading?: boolean;
  error?: string;
  success?: boolean;
}

export const RecoveryCard: React.FC<RecoveryCardProps> = ({
  onSubmit,
  isLoading = false,
  error,
  success = false
}) => {
  const { navigateToLogin } = useAuthNavigation();
  
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RecoveryFormData>({
    resolver: zodResolver(recoverySchema),
    defaultValues: {
      email: '',
    }
  });

  const handleFormSubmit: SubmitHandler<RecoveryFormData> = async (data) => {
    await onSubmit(data.email);
  };

  if (success) {
    return (
      <div className="space-y-6">
        <div className="p-6 rounded-lg bg-green-50 border border-green-200 text-center">
          <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-green-700 mb-2">
            Correo Enviado
          </h3>
          <p className="text-sm text-green-600 mb-4">
            Hemos enviado un enlace de recuperación a tu correo electrónico.
          </p>
          <p className="text-xs text-green-500">
            Revisa tu bandeja de entrada y spam. El enlace expira en 24 horas.
          </p>
        </div>

        <div className="text-center">
          <button
            onClick={navigateToLogin}
            className="text-sm text-zinc-800 hover:text-zinc-600 transition-colors font-medium"
          >
            Volver al inicio de sesión
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {error && (
        <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
        <EmailInput
          {...register('email')}
          error={errors.email?.message}
          label="Correo electrónico"
          placeholder="tu@correo.com"
          autoComplete="email"
        />

        <LoginButton
          type="submit"
          className="w-full"
          isLoading={isLoading}
        >
          Enviar Enlace de Recuperación
        </LoginButton>
      </form>

      <div className="text-center space-y-4">
        <p className="text-sm text-slate-500">
          ¿Recordaste tu contraseña?
        </p>
        
        <button
          onClick={navigateToLogin}
          className="text-sm text-zinc-800 hover:text-zinc-600 transition-colors font-medium"
        >
          Volver al inicio de sesión
        </button>
      </div>

      <div className="text-center">
        <p className="text-xs text-slate-400">
          ¿Necesitas ayuda? Contacta al administrador del sistema
        </p>
      </div>
    </div>
  );
};