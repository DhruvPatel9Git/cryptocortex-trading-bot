# Assignment 1 – Object, Context & Information Analysis  
**Student ID**: 202412066  
**Name**: Patel Dhruv Alkeshbhai  

## Project Title: CryptoCortex – Crypto Trading Platform

CryptoCortex is a secure, credit-based cryptocurrency trading platform that allows users to buy, sell, and transfer digital assets. It integrates credit management, portfolio tracking, real-time trading, and AI-powered chatbot assistance under a modular and scalable architecture using FastAPI, Beanie, MongoDB, and React.

---

## OBJECTS

| Object               | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `User`               | Registered platform user with credentials and a credit wallet              |
| `Stock`              | Represents a crypto asset available for trading (e.g., BTC, ETH)           |
| `Order`              | Buy or sell request submitted by a user                                    |
| `Transaction`        | Record of completed trades (buy/sell/transfer)                              |
| `Portfolio`          | Tracks user holdings for each crypto symbol                                |
| `Cart`               | Temporary collection of user trade actions (before final confirmation)     |
| `CartItem`           | Individual asset trade request in the cart                                 |
| `CreditsHistory`     | Logs changes to user credit balance with reasons                            |
| `ChatbotInteraction` | Stores user queries and AI-generated responses                             |
| `Cache`              | Stores frequently accessed or temporary data (e.g., symbol lookups)        |

---

## CONTEXTS

| Context               | Objects Involved                                    | Description                                                                 |
|-----------------------|-----------------------------------------------------|-----------------------------------------------------------------------------|
| User Authentication   | User                                                | Handles user registration, login, JWT token management                      |
| Credit Management     | User, CreditsHistory                                | Users spend credits for trades; tracks all credit usage and additions      |
| Trading Flow          | Stock, Order, Transaction, Portfolio, Cart, CartItem| Allows users to create and finalize trade orders using available credits   |
| Portfolio Tracking    | Portfolio, Transaction, User                        | Maintains user’s crypto holdings; updated after trades                     |
| Transaction History   | Transaction, Order, Stock                           | Full log of user transactions and details                                  |
| Cart Checkout         | Cart, CartItem, Portfolio, Transaction              | Batches multiple trade actions for execution                               |
| Chatbot System        | ChatbotInteraction                                  | AI assistant for trading help, market queries, and FAQs                    |
| Symbol Management     | Stock, Cache                                        | Dynamic price fetching and crypto symbol metadata                          |
| Real-Time Trading     | Order, Stock, Transaction                           | Live trades executed via async workers                                     |

---

## INFORMATION PER CONTEXT

### 1. User Authentication
- **User**: ID, Username, Email, Password (hashed), Role, JWT Tokens  
- **Session**: Last Login Time, Expiry, Refresh Tokens

### 2. Credit Management
- **CreditsHistory**:  
  - `user_id`, `amount`, `type` (`buy`, `bonus`, `refund`), `symbol`, `reason`, `timestamp`  
- **User Credit Balance**: Total available credits

### 3. Trading Flow
- **Order**:  
  - `order_id`, `user_id`, `stock_symbol`, `action` (`buy/sell`), `quantity`, `price`, `status`, `created_at`  
- **CartItem**:  
  - `cart_id`, `symbol`, `qty`, `price`, `action`, `fee`, `added_at`  
- **Transaction**:  
  - `transaction_id`, `user_id`, `symbol`, `order_type`, `price`, `qty`, `total`, `timestamp`  
- **Portfolio**:  
  - `user_id`, `symbol`, `balance`, `last_updated`  

### 4. Portfolio Tracking
- **Asset Aggregation**: Total holdings by symbol
- **Valuation**: Holdings × real-time market price (via cache or API)

### 5. Transaction History
- Filtered by: `user_id`, `symbol`, `order_type`, `date_range`

### 6. Cart Checkout
- Batch cart items into final trade confirmation
- On success:
  - Deduct credits
  - Update portfolio
  - Create transactions
  - Log in `CreditsHistory`

### 7. Chatbot System
- **ChatbotInteraction**:  
  - `user_id`, `query`, `response`, `timestamp`, `intent`, `matched_action`

### 8. Symbol Management
- **Stock**:  
  - `symbol`, `name`, `current_price`, `24h_volume`, `is_active`  
- **Cache**:  
  - Cached price, last updated timestamp

### 9. Real-Time Trading
- Queue workers handle background order execution
- Redis or RQ/Dramatiq backend used for async task handling


