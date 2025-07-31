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

Here's a complete **Markdown guide** for setting up a MongoDB database using **MongoDB Atlas**:

---

```markdown
# 🗄️ Setting Up MongoDB Atlas Database for CryptoCortex

This guide walks you through creating a **MongoDB Atlas** cluster, database, and user for your project.

---

## 1️⃣ Sign Up or Log In

🔗 Go to: [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)

- Sign up for a **free account** or log in if you already have one.

---

## 2️⃣ Create a New Project

1. Click **"New Project"** on your dashboard.
2. Enter a project name (e.g., `CryptoCortex`) and click **Next**.
3. Skip adding members or invite team members if needed.
4. Click **Create Project**.

---

## 3️⃣ Build a Cluster

1. Click **"Build a Database"**.
2. Select **Shared Cluster** (Free tier).
3. Choose:
   - Cloud Provider: `AWS`, `GCP`, or `Azure`
   - Region: Pick a region close to your location
4. Click **Create Cluster** (this may take a few minutes).

---

## 4️⃣ Create a Database User

1. In the cluster dashboard, go to **Database Access** → **+ Add New Database User**.
2. Set:
   - Username: `cryptouser`
   - Password: Choose a secure password (you’ll use this in `.env`)
3. Set **Database User Privileges** → Role: `Read and write to any database`.
4. Click **Add User**.

---

## 5️⃣ Whitelist Your IP Address

1. Go to **Network Access** → **+ Add IP Address**.
2. Select:
   - `Add your current IP address` (or `0.0.0.0/0` to allow all — not recommended for production).
3. Click **Confirm**.

---

## 6️⃣ Get Your Connection URI

1. Go to **Database** → Click **Connect** → Select **Connect your application**.
2. Copy the connection string that looks like this:

```

mongodb+srv://cryptouser:<password>@cluster0.mongodb.net/?retryWrites=true\&w=majority

````

3. Replace `<password>` with your actual password.

---

## 7️⃣ Update Your `.env` File

In the root of your project, update `.env`:

```env
MONGO_URI=mongodb+srv://cryptouser:<your_password>@cluster0.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=cryptocortex
````

---

✅ Now you're connected to your remote MongoDB Atlas database!

---

## 🧪 Test the Connection

Run your FastAPI backend:

```bash
uvicorn main:app --reload
```



---

Let me know if you'd like a version with screenshots or want to add Docker support with Atlas!
```

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

