# 📦 CryptoCortex Installation Guide

Welcome to the **CryptoCortex** installation guide. Follow these steps to set up the project on your local machine.

---

## 🚀 Prerequisites

Make sure you have the following installed:

- Python 3.9+
- Node.js 16+
- npm or yarn
- MongoDB
- Redis
- Git

---

## 🛠 Backend Setup (FastAPI + Beanie)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/cryptocortex.git
cd cryptocortex
2. Create a Virtual Environment
bash
Copy
Edit
python -m venv env
# Activate the environment
source env/bin/activate        # macOS/Linux
# OR
env\Scripts\activate           # Windows
3. Install Python Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Create a .env File in the root directory
env
Copy
Edit
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=cryptocortex
SECRET_KEY=your_secret_key
REDIS_URL=redis://localhost:6379
5. Run the Backend Server
bash
Copy
Edit
uvicorn main:app --reload
🌐 Frontend Setup (React)
1. Navigate to the Frontend Directory
bash
Copy
Edit
cd frontend
2. Install Node Dependencies
bash
Copy
Edit
npm install
# or
yarn install
3. Run the React Dev Server
bash
Copy
Edit
npm start
# or
yarn start
⚙️ Background Worker (Dramatiq + Redis)
1. Start Redis Server
Make sure Redis is running locally:

bash
Copy
Edit
redis-server
2. Start Dramatiq Worker
In a new terminal (while Redis and FastAPI are running):

bash
Copy
Edit
dramatiq tasks.trade_tasks --watch .
