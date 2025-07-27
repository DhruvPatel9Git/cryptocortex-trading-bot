import React from 'react';
import { useTheme } from './ThemeContext';
import styles from './ThemeToggle.module.css';

import sunIcon from '../assets/sun-icon.svg';
import moonIcon from '../assets/moon-icon.svg';

const ThemeToggle = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className={`${styles.themeToggle} ${theme === 'dark' ? styles.themeToggleDark : styles.themeToggleLight}`}
      aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
      title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
    >
      <img
        src={theme === 'dark' ? sunIcon : moonIcon}
        alt={theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'}
        className={styles.icon}
      />
    </button>
  );
};

export default ThemeToggle;
