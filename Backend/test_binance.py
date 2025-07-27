# binance_ping_test.py

from binance.client import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Binance API credentials
BINANCE_API_KEY = "YOO4ljLB435Z4ijKwKdOT5pLLk1ofE9WPbBsk9FFserVVeZedyyQ8OL5I1DvdE0y"
BINANCE_SECRET_KEY = "YqxtRhUnBRMi0Qggn4x8NUfaZzYDxbxxMiy9tb8T0rIL0mJycZJaS9HnMKmWlQdY"
TESTNET_API_URL = "https://testnet.binance.vision/api"


def get_binance_client():
    client = Client(
        api_key=BINANCE_API_KEY,
        api_secret=BINANCE_SECRET_KEY,
        testnet=True
    )
    client.API_URL = TESTNET_API_URL
    return client


def ping_binance():
    try:
        client = get_binance_client()
        client.ping()
        return True
    except Exception as e:
        print(f"[Binance] ⚠️ Ping failed: {e}")
        return False


def main():
    print("Testing Binance Ping...")

    success = ping_binance()

    if success:
        print("✅ Binance testnet is reachable!")
        client = get_binance_client()
        # Optionally fetch something to verify
        account_info = client.get_account()
        print("✅ Account fetched successfully!")
        print(account_info)
    else:
        print("❌ Binance testnet is unreachable. Check API keys, network, or Binance status.")


if __name__ == "__main__":
    main()
