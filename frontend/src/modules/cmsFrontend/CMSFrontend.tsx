// frontend/src/modules/cmsFrontend/CMSFrontend.tsx
import React from 'react';
import { ThemeProvider } from './context/ThemeContext';
import { HomePage } from './pages/HomePage';

export const CMSFrontend: React.FC = () => {
  return (
    <ThemeProvider>
      <HomePage />
    </ThemeProvider>
  );
};