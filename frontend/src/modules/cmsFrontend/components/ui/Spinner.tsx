// src/modules/cmsFrontend/components/ui/Spinner.tsx
import React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '../../utils/cn'

const spinnerVariants = cva(
  'animate-spin rounded-full border-2 border-current border-t-transparent',
  {
    variants: {
      size: {
        sm: 'h-4 w-4',
        default: 'h-6 w-6',
        lg: 'h-8 w-8',
        xl: 'h-12 w-12'
      },
      variant: {
        default: 'text-zinc-600 dark:text-zinc-400',
        primary: 'text-primary-600',
        white: 'text-white',
        current: 'text-current'
      }
    },
    defaultVariants: {
      size: 'default',
      variant: 'default'
    }
  }
)

export interface SpinnerProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof spinnerVariants> {
  label?: string
}

const Spinner = React.forwardRef<HTMLDivElement, SpinnerProps>(
  ({ className, size, variant, label, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn('flex items-center justify-center', className)}
        {...props}
      >
        <div 
          className={cn(spinnerVariants({ size, variant }))}
          aria-label={label || 'Cargando...'}
        />
        {label && (
          <span className="ml-2 text-sm text-zinc-600 dark:text-zinc-400">
            {label}
          </span>
        )}
      </div>
    )
  }
)

Spinner.displayName = 'Spinner'

// Loading overlay component
interface LoadingOverlayProps {
  isLoading: boolean
  label?: string
  backdrop?: boolean
  className?: string
}

const LoadingOverlay: React.FC<LoadingOverlayProps> = ({
  isLoading,
  label = 'Cargando...',
  backdrop = true,
  className
}) => {
  if (!isLoading) return null

  return (
    <div className={cn(
      'absolute inset-0 flex items-center justify-center z-50',
      backdrop && 'bg-white/80 dark:bg-zinc-900/80 backdrop-blur-sm',
      className
    )}>
      <div className="flex flex-col items-center gap-3">
        <Spinner size="lg" variant="primary" />
        <p className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
          {label}
        </p>
      </div>
    </div>
  )
}

// Page loading component
const PageLoader: React.FC<{ label?: string }> = ({ 
  label = 'Cargando contenido...' 
}) => {
  return (
    <div className="flex items-center justify-center min-h-[400px]">
      <div className="flex flex-col items-center gap-4">
        <Spinner size="xl" variant="primary" />
        <div className="text-center">
          <p className="text-lg font-medium text-zinc-700 dark:text-zinc-300">
            {label}
          </p>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">
            Esto solo tomará un momento
          </p>
        </div>
      </div>
    </div>
  )
}

export { Spinner, LoadingOverlay, PageLoader, spinnerVariants }