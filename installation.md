# 💹 Installation Guide for CryptoCortex

CryptoCortex is a full-stack cryptocurrency trading platform powered by FastAPI (backend) and React (frontend). This guide will walk you through setting up the project on your local machine.

---

## 📋 Prerequisites

Ensure you have the following installed on your system:

- **Python 3.9+**
- **Node.js + npm (or yarn)**
- **MongoDB** (locally or Atlas)
- **Redis**
- **Git**

---

## 🧠 Backend Setup (FastAPI)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/cryptocortex.git
cd cryptocortex
```

---

### 2️⃣ Create a Virtual Environment

#### 🔸 On Windows:

```bash
python -m venv env
env\Scripts\activate
```

#### 🔸 On macOS/Linux:

```bash
python3 -m venv env
source env/bin/activate
```

---

### 3️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

✅ This installs all backend packages listed in `requirements.txt`.

---

### 4️⃣ Create a `.env` File

Create a `.env` file in the root directory and add the following:

```env
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=cryptocortex

# Security
SECRET_KEY=your_secret_key

# Redis Configuration
REDIS_URL=redis://localhost:6379
```

🔐 Replace `your_secret_key` with a strong secret.
🗂️ Ensure `.env` is listed in `.gitignore`.

---

### 5️⃣ Run the FastAPI Backend Server

```bash
uvicorn main:app --reload
```

You should see output like:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 🌐 Frontend Setup (React)

### 1️⃣ Navigate to Frontend Directory

```bash
cd frontend
```

---

### 2️⃣ Install Node Dependencies

```bash
npm install
# or
yarn install
```

---

### 3️⃣ Run the React Dev Server

```bash
npm start
# or
yarn start
```

✅ The app should now be running on `http://localhost:3000`.

---

## ⚙️ Background Worker (Dramatiq + Redis)

### 1️⃣ Start Redis Server

Make sure Redis is installed and running:

```bash
redis-server
```

---

### 2️⃣ Start the Dramatiq Worker

In a new terminal, with your virtual environment active:

```bash
dramatiq tasks.trade_tasks --watch .
```

✅ This enables background processing for trade-related tasks.

---

## ✅ Summary of Commands

| Step                    | Command                                                       |
| ----------------------- | ------------------------------------------------------------- |
| Clone Repo              | `git clone https://github.com/your-username/cryptocortex.git` |
| Activate venv (Linux)   | `source env/bin/activate`                                     |
| Activate venv (Windows) | `env\Scripts\activate`                                        |
| Install Python Deps     | `pip install -r requirements.txt`                             |
| Run Backend             | `uvicorn main:app --reload`                                   |
| Run Frontend            | `cd frontend && npm start`                                    |
| Start Redis             | `redis-server`                                                |
| Start Worker            | `dramatiq tasks.trade_tasks --watch .`                        |

---

## 🧪 Test the Setup

* Backend: Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for FastAPI Swagger docs.
* Frontend: Visit [http://localhost:3000](http://localhost:3000)
* Check logs for Redis and Dramatiq worker

---

