// modules/auth/components/LoginCard.tsx
import React from 'react';
import { useForm, type SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

import { EmailInput } from '../ui/inputs/EmailInput';
import { PasswordInput } from '../ui/inputs/PasswordInput';
import { LoginButton } from '../ui/buttons/LoginButton';
import { GoogleLoginButton } from '../ui/buttons/GoogleLoginButton';
import { useAuthNavigation } from '../context/AuthNavigationContext';

const loginSchema = z.object({
  identifier: z.string().min(1, 'El correo o usuario es requerido'),
  password: z.string().min(1, 'La contraseña es requerida'),
  remember_me: z.boolean(),
});

type LoginFormData = z.infer<typeof loginSchema>;

interface LoginCardProps {
  onSubmit: (data: LoginFormData) => Promise<void>;
  onGoogleLogin?: () => void;
  isLoading?: boolean;
  error?: string;
}

export const LoginCard: React.FC<LoginCardProps> = ({
  onSubmit,
  onGoogleLogin,
  isLoading = false,
  error
}) => {
  const { navigateToRecovery } = useAuthNavigation();
  
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      identifier: '',
      password: '',
      remember_me: false,
    }
  });

  const handleFormSubmit: SubmitHandler<LoginFormData> = async (data) => {
    await onSubmit(data);
  };

  return (
    <div className="space-y-6">
      {/* OAuth Options */}
      {onGoogleLogin && (
        <div className="space-y-4">
          <GoogleLoginButton onClick={onGoogleLogin} isLoading={isLoading} />
          
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-200" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-white text-slate-500">o continúa con</span>
            </div>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
          {error}
        </div>
      )}

      {/* Login Form */}
      <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
        <EmailInput
          {...register('identifier')}
          error={errors.identifier?.message}
          label="Correo o nombre de usuario"
          autoComplete="username"
        />

        <PasswordInput
          {...register('password')}
          error={errors.password?.message}
          autoComplete="current-password"
        />

        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              {...register('remember_me')}
              type="checkbox"
              className="h-4 w-4 rounded border-slate-300 text-zinc-800 focus:ring-zinc-500 focus:ring-offset-0"
            />
            <label className="ml-2 text-sm text-slate-600">
              Mantener sesión iniciada
            </label>
          </div>

          <button
            type="button"
            onClick={navigateToRecovery}
            className="text-sm text-zinc-800 hover:text-zinc-600 transition-colors font-medium"
          >
            ¿Olvidaste tu contraseña?
          </button>
        </div>

        <LoginButton
          type="submit"
          className="w-full"
          isLoading={isLoading}
        >
          Iniciar Sesión
        </LoginButton>
      </form>

      {/* Footer */}
      <div className="text-center text-sm text-slate-500">
        ¿Necesitas una cuenta?{' '}
        <button className="text-zinc-800 hover:text-zinc-600 transition-colors font-medium">
          Contacta al administrador
        </button>
      </div>
    </div>
  );
};