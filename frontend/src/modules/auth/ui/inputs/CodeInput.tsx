// modules/auth/ui/inputs/CodeInput.tsx
import React, { forwardRef, useEffect, useRef } from 'react';
import { cn } from '../../../../shared/utils';

interface CodeInputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'value' | 'onChange'> {
  length?: number;
  value: string;
  onChange: (value: string) => void;
  error?: string;
}

export const CodeInput = forwardRef<HTMLInputElement, CodeInputProps>(
  ({ length = 6, value, onChange, error, className, ...props }, ref) => {
    const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

    useEffect(() => {
      if (inputRefs.current[0]) {
        inputRefs.current[0].focus();
      }
    }, []);

    const handleChange = (index: number, inputValue: string) => {
      const newValue = value.split('');
      newValue[index] = inputValue.slice(-1);
      const updatedValue = newValue.join('');
      onChange(updatedValue);

      if (inputValue && index < length - 1) {
        inputRefs.current[index + 1]?.focus();
      }
    };

    const handleKeyDown = (index: number, e: React.KeyboardEvent) => {
      if (e.key === 'Backspace' && !value[index] && index > 0) {
        inputRefs.current[index - 1]?.focus();
      }
    };

    const handlePaste = (e: React.ClipboardEvent) => {
      e.preventDefault();
      const pastedData = e.clipboardData.getData('text').slice(0, length);
      onChange(pastedData);
    };

    return (
      <div className="space-y-2">
        <label className="block text-sm font-medium text-slate-700">
          Código de verificación
        </label>
        <div className="flex gap-3 justify-center">
          {Array.from({ length }, (_, index) => (
            <input
              key={index}
              ref={(el) => {
                inputRefs.current[index] = el;
                if (index === 0 && ref && typeof ref === 'function') {
                  ref(el);
                } else if (index === 0 && ref && 'current' in ref) {
                  ref.current = el;
                }
              }}
              type="text"
              inputMode="numeric"
              maxLength={1}
              value={value[index] || ''}
              onChange={(e) => handleChange(index, e.target.value)}
              onKeyDown={(e) => handleKeyDown(index, e)}
              onPaste={handlePaste}
              className={cn(
                "w-12 h-12 text-center text-xl font-mono rounded-lg border bg-white text-slate-800 shadow-sm",
                "focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent",
                "transition-all duration-200",
                error ? "border-red-400 focus:ring-red-400" : "border-slate-300",
                className
              )}
              {...props}
            />
          ))}
        </div>
        {error && (
          <p className="text-sm text-red-500 flex items-center justify-center gap-1">
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

CodeInput.displayName = 'CodeInput';