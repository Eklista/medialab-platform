// shared/utils/cn.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// shared/utils/index.ts
export * from './cn';
export * from './constants';
export * from './formatting';
export * from './validation';