import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import CryptoListPage from './components/CryptoListPage';
import CryptoCandlesTable from './components/CryptoCandlesTable';
import Portfolio from './components/Portfolio';
import Register from './components/Register';
import Login from './components/Login';
import BuySellTransferPage from './components/BuySellTransfer';
import Navbar from './components/Navbar';
import CryptoDetailPage from './components/CryptoDetailPage';
import ChatWidget from './components/ChatWidget';  
import styles from './App.module.css'; 


const AppContent = () => {
  const location = useLocation();


  const hideUI = ['/login', '/register'].includes(location.pathname);

  return (
    <>
      {!hideUI && <Navbar />}

      <div className={styles.mainContent}>
        <Routes>
          <Route path="/" element={<CryptoListPage />} />
          <Route path="/candles/:symbol" element={<CryptoCandlesTable />} />
          <Route path="/portfolio" element={<Portfolio />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/trade" element={<BuySellTransferPage />} />
          <Route path="/details" element={<CryptoDetailPage />} />  
        </Routes>
      </div>

      {!hideUI && <ChatWidget />}
    </>
  );
};

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
