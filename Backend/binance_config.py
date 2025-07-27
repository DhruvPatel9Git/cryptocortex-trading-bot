from binance.client import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Binance API credentials
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# Initialize Binance client
client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY, testnet=True)
client.API_URL = "https://testnet.binance.vision/api"

