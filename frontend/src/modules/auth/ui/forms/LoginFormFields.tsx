// modules/auth/ui/forms/LoginFormFields.tsx
import React from 'react';
import type { UseFormRegister, FieldErrors } from 'react-hook-form';
import { EmailInput } from '../inputs/EmailInput';
import { PasswordInput } from '../inputs/PasswordInput';

interface LoginFormData {
  identifier: string;
  password: string;
  remember_me: boolean;
}

interface LoginFormFieldsProps {
  register: UseFormRegister<LoginFormData>;
  errors: FieldErrors<LoginFormData>;
}

export const LoginFormFields: React.FC<LoginFormFieldsProps> = ({
  register,
  errors
}) => {
  return (
    <>
      <EmailInput
        {...register('identifier')}
        error={errors.identifier?.message}
        label="Correo o nombre de usuario"
        placeholder="tu@correo.com"
        autoComplete="username"
      />

      <PasswordInput
        {...register('password')}
        error={errors.password?.message}
        label="Contraseña"
        autoComplete="current-password"
      />

      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <input
            {...register('remember_me')}
            type="checkbox"
            className="h-4 w-4 rounded border-zinc-700 bg-zinc-900 text-lime-400 focus:ring-lime-400 focus:ring-offset-zinc-950"
          />
          <label className="ml-2 text-sm text-zinc-300">
            Mantener sesión iniciada
          </label>
        </div>

        <button
          type="button"
          onClick={() => window.location.href = '/recovery'}
          className="text-sm text-lime-400 hover:text-lime-300 transition-colors"
        >
          ¿Olvidaste tu contraseña?
        </button>
      </div>
    </>
  );
};