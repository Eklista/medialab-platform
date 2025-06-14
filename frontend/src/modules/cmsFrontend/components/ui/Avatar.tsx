// src/modules/cmsFrontend/components/ui/Avatar.tsx
import React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '../../utils/cn'

const avatarVariants = cva(
  'relative flex shrink-0 overflow-hidden rounded-full bg-zinc-100 dark:bg-zinc-800',
  {
    variants: {
      size: {
        sm: 'h-8 w-8',
        default: 'h-10 w-10',
        lg: 'h-12 w-12',
        xl: 'h-16 w-16',
        '2xl': 'h-20 w-20'
      }
    },
    defaultVariants: {
      size: 'default'
    }
  }
)

export interface AvatarProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof avatarVariants> {
  src?: string
  alt?: string
  fallback?: string
}

const Avatar = React.forwardRef<HTMLDivElement, AvatarProps>(
  ({ className, size, src, alt, fallback, ...props }, ref) => {
    const [imageError, setImageError] = React.useState(false)
    
    const handleImageError = () => {
      setImageError(true)
    }

    const getInitials = (name?: string) => {
      if (!name) return '??'
      return name
        .split(' ')
        .map(part => part.charAt(0))
        .join('')
        .toUpperCase()
        .slice(0, 2)
    }

    return (
      <div
        ref={ref}
        className={cn(avatarVariants({ size }), className)}
        {...props}
      >
        {src && !imageError ? (
          <img
            src={src}
            alt={alt || 'Avatar'}
            className="aspect-square h-full w-full object-cover"
            onError={handleImageError}
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center bg-zinc-200 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-300 font-medium text-sm">
            {getInitials(fallback || alt)}
          </div>
        )}
      </div>
    )
  }
)

Avatar.displayName = 'Avatar'

// Avatar with status indicator
interface AvatarWithStatusProps extends AvatarProps {
  status?: 'online' | 'offline' | 'away' | 'busy'
  showStatus?: boolean
}

const AvatarWithStatus = React.forwardRef<HTMLDivElement, AvatarWithStatusProps>(
  ({ status = 'offline', showStatus = true, className, ...props }, ref) => {
    const statusColors = {
      online: 'bg-emerald-500',
      offline: 'bg-zinc-400',
      away: 'bg-amber-500',
      busy: 'bg-red-500'
    }

    return (
      <div className="relative">
        <Avatar ref={ref} className={className} {...props} />
        {showStatus && (
          <div className={cn(
            'absolute -bottom-0.5 -right-0.5 h-3 w-3 rounded-full border-2 border-white dark:border-zinc-900',
            statusColors[status]
          )} />
        )}
      </div>
    )
  }
)

AvatarWithStatus.displayName = 'AvatarWithStatus'

// Avatar Group for showing multiple users
interface AvatarGroupProps {
  users: Array<{
    id: string
    name: string
    avatar?: string
  }>
  max?: number
  size?: VariantProps<typeof avatarVariants>['size']
  className?: string
}

const AvatarGroup: React.FC<AvatarGroupProps> = ({
  users,
  max = 4,
  size = 'default',
  className
}) => {
  const visibleUsers = users.slice(0, max)
  const remainingCount = users.length - max

  return (
    <div className={cn('flex -space-x-2', className)}>
      {visibleUsers.map((user, index) => (
        <Avatar
          key={user.id}
          src={user.avatar}
          alt={user.name}
          fallback={user.name}
          size={size}
          className="border-2 border-white dark:border-zinc-900"
          style={{ zIndex: visibleUsers.length - index }}
        />
      ))}
      
      {remainingCount > 0 && (
        <div className={cn(
          avatarVariants({ size }),
          'border-2 border-white dark:border-zinc-900 bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center text-xs font-medium text-zinc-600 dark:text-zinc-300'
        )}>
          +{remainingCount}
        </div>
      )}
    </div>
  )
}

export { Avatar, AvatarWithStatus, AvatarGroup, avatarVariants }