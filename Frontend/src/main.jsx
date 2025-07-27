import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';
import { ThemeProvider } from './context/ThemeContext'; // ✅ make sure this is correct path

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ThemeProvider>    {/* ✅ wrap your app with ThemeProvider */}
      <App />
    </ThemeProvider>
  </StrictMode>
);
