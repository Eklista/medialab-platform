// modules/auth/ui/forms/TwoFactorFormFields.tsx
import React from 'react';
import { CodeInput } from '../inputs/CodeInput';

interface TwoFactorFormFieldsProps {
  code: string;
  onCodeChange: (code: string) => void;
  error?: string;
  timeLeft: number;
  formattedTime: string;
}

export const TwoFactorFormFields: React.FC<TwoFactorFormFieldsProps> = ({
  code,
  onCodeChange,
  error,
  timeLeft,
  formattedTime
}) => {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <div className={`text-sm font-medium ${timeLeft < 60 ? 'text-red-400' : 'text-orange-400'}`}>
          Tiempo restante: {formattedTime}
        </div>
      </div>

      <CodeInput
        value={code}
        onChange={onCodeChange}
        error={error}
        length={6}
        autoFocus
      />

      <div className="text-center space-y-2">
        <p className="text-sm text-zinc-400">
          Ingresa el código de 6 dígitos de tu aplicación autenticadora
        </p>
        
        <button
          type="button"
          onClick={() => window.location.href = '/login'}
          className="text-sm text-lime-400 hover:text-lime-300 transition-colors"
        >
          Volver al inicio de sesión
        </button>
      </div>

      <div className="text-center">
        <button
          type="button"
          className="text-xs text-zinc-500 hover:text-zinc-400 transition-colors"
        >
          ¿No tienes acceso a tu dispositivo? Usa un código de respaldo
        </button>
      </div>
    </div>
  );
};