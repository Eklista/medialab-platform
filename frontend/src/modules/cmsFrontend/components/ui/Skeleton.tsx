// src/modules/cmsFrontend/components/ui/Skeleton.tsx
import React from 'react'
import { cn } from '../../utils/cn'

interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'circular' | 'text'
}

const Skeleton = React.forwardRef<HTMLDivElement, SkeletonProps>(
  ({ className, variant = 'default', ...props }, ref) => {
    const baseClasses = 'animate-pulse bg-zinc-200 dark:bg-zinc-800'
    
    const variantClasses = {
      default: 'rounded-lg',
      circular: 'rounded-full',
      text: 'rounded h-4'
    }

    return (
      <div
        ref={ref}
        className={cn(baseClasses, variantClasses[variant], className)}
        {...props}
      />
    )
  }
)

Skeleton.displayName = 'Skeleton'

// Componentes preconfigurados para casos comunes
const SkeletonCard = () => (
  <div className="space-y-3">
    <Skeleton className="h-48 w-full" />
    <div className="space-y-2">
      <Skeleton variant="text" className="w-3/4" />
      <Skeleton variant="text" className="w-1/2" />
    </div>
  </div>
)

const SkeletonVideo = () => (
  <div className="space-y-3">
    <Skeleton className="aspect-video w-full" />
    <div className="space-y-2">
      <Skeleton variant="text" className="w-5/6" />
      <div className="flex items-center gap-2">
        <Skeleton variant="circular" className="h-6 w-6" />
        <Skeleton variant="text" className="w-24" />
        <Skeleton variant="text" className="w-16" />
      </div>
    </div>
  </div>
)

const SkeletonGallery = () => (
  <div className="space-y-3">
    <Skeleton className="aspect-square w-full" />
    <div className="space-y-2">
      <Skeleton variant="text" className="w-4/5" />
      <div className="flex items-center justify-between">
        <Skeleton variant="text" className="w-20" />
        <Skeleton variant="text" className="w-16" />
      </div>
    </div>
  </div>
)

const SkeletonFaculty = () => (
  <div className="space-y-4">
    <Skeleton className="h-32 w-full" />
    <div className="space-y-2">
      <Skeleton variant="text" className="w-3/4" />
      <Skeleton variant="text" className="w-1/2" />
      <div className="flex gap-2 mt-3">
        <Skeleton className="h-6 w-16 rounded-full" />
        <Skeleton className="h-6 w-20 rounded-full" />
      </div>
    </div>
  </div>
)

export { 
  Skeleton, 
  SkeletonCard, 
  SkeletonVideo, 
  SkeletonGallery, 
  SkeletonFaculty 
}