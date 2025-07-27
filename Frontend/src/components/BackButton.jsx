import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '../styles/BackButton.module.css';  // We'll add this next

const BackButton = () => {
  const navigate = useNavigate();

  return (
    <button className={styles.backButton} onClick={() => navigate(-1)}>
      ⬅ Back
    </button>
  );
};

export default BackButton;
