// modules/auth/ui/inputs/EmailInput.tsx
import React, { forwardRef } from 'react';
import { cn } from '../../../../shared/utils';

interface EmailInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
  label?: string;
}

export const EmailInput = forwardRef<HTMLInputElement, EmailInputProps>(
  ({ error, label = "Correo electrónico", className, ...props }, ref) => {
    return (
      <div className="space-y-2">
        <label className="block text-sm font-medium text-zinc-200">
          {label}
        </label>
        <input
          ref={ref}
          type="email"
          className={cn(
            "w-full h-11 px-4 rounded-lg border bg-zinc-900 text-zinc-50 placeholder:text-zinc-500",
            "focus:outline-none focus:ring-2 focus:ring-lime-400 focus:border-transparent",
            "transition-all duration-200",
            error ? "border-red-500" : "border-zinc-700",
            className
          )}
          placeholder="tu@correo.com"
          {...props}
        />
        {error && (
          <p className="text-sm text-red-400 flex items-center gap-1">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            {error}
          </p>
        )}
      </div>
    );
  }
);

EmailInput.displayName = 'EmailInput';