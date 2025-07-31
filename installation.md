Here's your **complete and properly formatted Markdown file** for setting up **CryptoCortex**, including backend, frontend, MongoDB Atlas, Redis, and Dramatiq:

---

````markdown
# 💹 Installation Guide for CryptoCortex

CryptoCortex is a full-stack cryptocurrency trading platform powered by **FastAPI** (backend) and **React** (frontend). This guide walks you through setting up the project on your local machine.

---

## 📋 Prerequisites

Ensure you have the following installed:

- **Python 3.9+**
- **Node.js + npm** (or **yarn**)
- **MongoDB** (locally or via **Atlas**)
- **Redis**
- **Git**

---

## 🧠 Backend Setup (FastAPI)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/cryptocortex.git
cd cryptocortex
```
````

> Replace `your-username` with your actual GitHub username.

---

### 2️⃣ Create a Virtual Environment

#### 🔹 On Windows:

```bash
python -m venv env
env\Scripts\activate
```

#### 🔹 On macOS/Linux:

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

### 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

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

You should see:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 🗄️ Setting Up MongoDB Atlas (Optional)

If using **MongoDB Atlas** instead of local MongoDB:

### 1. Sign Up or Log In

🔗 [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)

---

### 2. Create a Project & Cluster

* Create new project (e.g., `CryptoCortex`)
* Create **Shared Cluster (Free tier)**

---

### 3. Create Database User

* Username: `cryptouser`
* Password: your choice
* Role: **Read and write to any database**

---

### 4. Whitelist Your IP

* Add your current IP or `0.0.0.0/0` (not recommended for production)

---

### 5. Get Connection URI

```text
mongodb+srv://cryptouser:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
```

> Replace `<password>` with your actual password

---

### 6. Update `.env` for Atlas

```env
MONGO_URI=mongodb+srv://cryptouser:<your_password>@cluster0.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=cryptocortex
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

### 3️⃣ Run React Dev Server

```bash
npm start
# or
yarn start
```

✅ Visit: [http://localhost:3000](http://localhost:3000)

---

## ⚙️ Background Worker (Dramatiq + Redis)

### 1️⃣ Start Redis Server

```bash
redis-server
```

> Ensure Redis is installed and running.

---

### 2️⃣ Start Dramatiq Worker

```bash
dramatiq tasks.trade_tasks --watch .
```

✅ This enables background task processing during development.

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

## 🧪 Testing the Setup

* **Backend Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Frontend App**: [http://localhost:3000](http://localhost:3000)
* **Worker Logs**: Watch terminal where Dramatiq is running
* **Redis Status**: Confirm Redis is actively running

---

## 📄 License

This project is licensed under the **MIT License**.
See the `LICENSE` file for details.

```


