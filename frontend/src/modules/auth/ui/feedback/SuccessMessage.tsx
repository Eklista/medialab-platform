// modules/auth/ui/feedback/SuccessMessage.tsx
import React from 'react';
import { cn } from '../../../../shared/utils';

interface SuccessMessageProps {
  message: string;
  className?: string;
  dismissible?: boolean;
  onDismiss?: () => void;
}

export const SuccessMessage: React.FC<SuccessMessageProps> = ({
  message,
  className,
  dismissible = false,
  onDismiss
}) => {
  return (
    <div className={cn(
      "p-4 rounded-lg bg-green-50 border border-green-200 text-green-700 text-sm",
      "flex items-start gap-3",
      className
    )}>
      <svg className="w-5 h-5 flex-shrink-0 mt-0.5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
      </svg>
      
      <div className="flex-1">
        {message}
      </div>
      
      {dismissible && onDismiss && (
        <button
          onClick={onDismiss}
          className="text-green-500 hover:text-green-600 transition-colors flex-shrink-0"
        >
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      )}
    </div>
  );
};