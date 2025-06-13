// modules/auth/ui/forms/RecoveryFormFields.tsx
import React from 'react';
import type { UseFormRegister, FieldErrors } from 'react-hook-form';
import { EmailInput } from '../inputs/EmailInput';

interface RecoveryFormData {
  email: string;
}

interface RecoveryFormFieldsProps {
  register: UseFormRegister<RecoveryFormData>;
  errors: FieldErrors<RecoveryFormData>;
}

export const RecoveryFormFields: React.FC<RecoveryFormFieldsProps> = ({
  register,
  errors
}) => {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <p className="text-sm text-zinc-400 mb-6">
          Ingresa tu correo electrónico y te enviaremos un enlace para restablecer tu contraseña.
        </p>
      </div>

      <EmailInput
        {...register('email')}
        error={errors.email?.message}
        label="Correo electrónico"
        placeholder="tu@correo.com"
        autoComplete="email"
      />

      <div className="text-center space-y-4">
        <p className="text-sm text-zinc-400">
          ¿Recordaste tu contraseña?
        </p>
        
        <button
          type="button"
          onClick={() => window.location.href = '/login'}
          className="text-sm text-lime-400 hover:text-lime-300 transition-colors"
        >
          Volver al inicio de sesión
        </button>
      </div>
    </div>
  );
};