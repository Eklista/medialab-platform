// modules/auth/ui/feedback/ErrorMessage.tsx
import React from 'react';
import { cn } from '../../../../shared/utils';

interface ErrorMessageProps {
  message: string;
  className?: string;
  dismissible?: boolean;
  onDismiss?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  message,
  className,
  dismissible = false,
  onDismiss
}) => {
  return (
    <div className={cn(
      "p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm",
      "flex items-start gap-3",
      className
    )}>
      <svg className="w-5 h-5 flex-shrink-0 mt-0.5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
      </svg>
      
      <div className="flex-1">
        {message}
      </div>
      
      {dismissible && onDismiss && (
        <button
          onClick={onDismiss}
          className="text-red-500 hover:text-red-600 transition-colors flex-shrink-0"
        >
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      )}
    </div>
  );
};