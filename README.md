
# 🪙 CryptoCortex  

CryptoCortex is a modern **crypto trading and portfolio management platform** built with **FastAPI**, **MongoDB (Beanie ODM)**, and a **React frontend**.  
It allows users to buy, sell, transfer, and manage cryptocurrencies while tracking balances, transaction history, and credits.  

---

## 🚀 Features  

- 🔑 **Authentication & Authorization**  
  - JWT-based login, registration, and refresh tokens  
  - Secure password hashing  

- 📈 **Trading & Portfolio**  
  - Buy & Sell crypto using trading symbols (e.g., `BTCUSDT`, `TRXUSDT`)  
  - Transfer assets between users  
  - Portfolio management with real-time updates  

- 🛒 **Cart & Credits System**  
  - Add multiple trades to a cart and checkout in bulk  
  - Manage credits for deposits, withdrawals, and trade settlements  
  - Full **credits history tracking**  

- 🔔 **Real-time Alerts**  
  - Low balance warnings  
  - Suspicious transaction detection  
  - Loan repayment deadline notifications (via **SSE + Observer Pattern**)  

- 📊 **Admin & Analytics**  
  - Transaction monitoring  
  - User management  
  - Trade analytics and reporting  

---

## 🛠️ Tech Stack  

### Backend  
- **FastAPI** (Python)  
- **Beanie ODM** + **MongoDB** (NoSQL database)  
- **JWT Authentication**  
- **Dramatiq** (task queue)  
- **Server-Sent Events (SSE)** for real-time alerts  

### Frontend  
- **React + TailwindCSS**  
- **ShadCN/UI components**  
- **Recharts** for data visualization  

---

## 📂 Project Structure  

```

cryptocortex/
│── backend/
│   ├── main.py                 # FastAPI entrypoint
│   ├── models/                 # MongoDB (Beanie) models
│   ├── routes/                 # API routes (trade, transfer, cart, credits, auth, etc.)
│   ├── utils/                  # Helpers (DB connection, JWT, hashing)
│   ├── services/               # Business logic
│   ├── observers/              # Observer pattern for alerts
│   ├── tasks/                  # Background jobs with Dramatiq
│
│── frontend/
│   ├── src/
│   │   ├── pages/              # React pages (Dashboard, BuySellTransferPage, etc.)
│   │   ├── components/         # Reusable UI components
│   │   ├── services/           # API calls & hooks
│   │   ├── App.jsx             # Main app entry
│
│── docs/                       # Documentation
│── README.md                   # Project README

````

---

## ⚡ Installation & Setup  

### 1. Clone the Repository  
```bash
git clone https://github.com/your-username/cryptocortex.git
cd cryptocortex
````

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 📌 API Endpoints

### 🔑 Auth

* `POST /auth/register` → Register user
* `POST /auth/login` → Login & get JWT
* `POST /auth/refresh` → Refresh token

### 💱 Trade

* `POST /trade/buy` → Buy crypto
* `POST /trade/sell` → Sell crypto
* `POST /transfer` → Transfer crypto

### 🛒 Cart

* `POST /cart/add` → Add trade to cart
* `POST /cart/checkout` → Process all trades in cart
* `GET /cart/view` → View cart
* `DELETE /cart/clear` → Clear cart

### 💳 Credits

* `GET /credits/balance` → View balance
* `POST /credits/deposit` → Deposit credits
* `GET /credits/history` → View transaction history

---

## 🔮 Roadmap

* [ ] Add support for real exchange APIs (Binance, Coinbase)
* [ ] Implement notifications via WebSocket + SSE hybrid
* [ ] Extend portfolio analytics (PnL, charts, risk metrics)
* [ ] Mobile app (React Native)

---

## 🤝 Contributing

Contributions are welcome!

* Fork the repo
* Create a new branch (`feature/my-feature`)
* Commit changes
* Open a Pull Request

---

## 📜 License

MIT License © 2025 \[Your Name / Team]

---

```

👉 Do you want me to also include **demo data & Postman collection docs** (for API testing), so anyone can quickly test `cart`, `credits`, `trade`, and `transfer` flows?
```
# CryptoCortex---Crypto-Trading-Bot
