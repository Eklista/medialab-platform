// src/modules/cmsFrontend/CMSRouter.tsx
import React from 'react'
import { ThemeProvider } from './context/ThemeContext'
import { HomePage } from './pages/HomePage'

// Simple router - HomePage handles all the intelligence
export const CMSRouter: React.FC = () => {
  return (
    <ThemeProvider>
      <HomePage />
    </ThemeProvider>
  )
}