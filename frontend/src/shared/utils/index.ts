/**
 * Shared Utils - Utility functions used across modules
 * Centralizes: formatting, validation, constants, helper functions
 */

import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
