# bybit_api.py
import httpx
import time
import hashlib
import hmac
import json
import logging

# 로깅 설정
logging.basicConfig(filename="trade_log.txt", level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class BybitAPI:
    def __init__(self, api_key: str, api_secret: str, base_url="https://api-testnet.bybit.com"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

    async def get_ticker_price(self, symbol: str):
        """ Get the latest price for a given symbol """
        url = f"{self.base_url}/v2/public/tickers"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params={"symbol": symbol})
                data = response.json()
                if "result" in data and data["result"]:
                    return float(data["result"][0]["last_price"])
        except Exception as e:
            logging.error(f"Error fetching ticker price: {e}")
        return None
    
    async def place_order(self, symbol: str, side: str, qty: float, order_type="Market"):
        """ Place an order on Bybit """
        timestamp = int(time.time() * 1000)
        params = {
            "api_key": self.api_key,
            "symbol": symbol,
            "side": side,
            "order_type": order_type,
            "qty": qty,
            "time_in_force": "GoodTillCancel",
            "timestamp": timestamp
        }
        query_string = "&".join([f"{key}={params[key]}" for key in sorted(params)])
        signature = hmac.new(
            self.api_secret.encode(), query_string.encode(), hashlib.sha256
        ).hexdigest()
        params["sign"] = signature

        url = f"{self.base_url}/v2/private/order/create"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=params)
                return response.json()
        except Exception as e:
            logging.error(f"Error placing order: {e}")
            return None

# trading_logic.py
from bybit_api import BybitAPI
import asyncio

async def get_spread(api, symbol1: str, symbol2: str):
    """ Calculate the spread between two assets """
    price1 = await api.get_ticker_price(symbol1)
    price2 = await api.get_ticker_price(symbol2)
    if price1 is not None and price2 is not None:
        return abs(price1 - price2)
    return None

async def generate_trade_signal(api, symbol1: str, symbol2: str, threshold: float):
    """ Generate a trade signal based on spread threshold """
    spread = await get_spread(api, symbol1, symbol2)
    if spread is not None:
        if spread > threshold:
            return "Sell BTC, Buy ETH"
        elif spread < -threshold:
            return "Buy BTC, Sell ETH"
        else:
            return "Hold"
    return "No data"

# gui.py
import tkinter as tk
from tkinter import messagebox
import asyncio
from bybit_api import BybitAPI
from trading_logic import get_spread, generate_trade_signal

class TradingApp:
    def __init__(self, root, api):
        self.api = api
        self.root = root
        self.root.title("Bybit Trading Bot")
        
        tk.Label(root, text="BTC Price:").grid(row=0, column=0)
        self.btc_price_label = tk.Label(root, text="Loading...")
        self.btc_price_label.grid(row=0, column=1)
        
        tk.Label(root, text="ETH Price:").grid(row=1, column=0)
        self.eth_price_label = tk.Label(root, text="Loading...")
        self.eth_price_label.grid(row=1, column=1)
        
        tk.Label(root, text="Spread:").grid(row=2, column=0)
        self.spread_label = tk.Label(root, text="Calculating...")
        self.spread_label.grid(row=2, column=1)
        
        tk.Button(root, text="Check Prices", command=self.update_prices).grid(row=3, column=0, columnspan=2)
        tk.Button(root, text="Trade", command=self.execute_trade).grid(row=4, column=0, columnspan=2)
        
        asyncio.run(self.update_prices())
    
    async def update_prices(self):
        btc_price = await self.api.get_ticker_price("BTCUSDT")
        eth_price = await self.api.get_ticker_price("ETHUSDT")
        spread = await get_spread(self.api, "BTCUSDT", "ETHUSDT")
        
        self.btc_price_label.config(text=f"{btc_price}")
        self.eth_price_label.config(text=f"{eth_price}")
        self.spread_label.config(text=f"{spread}")
        
    async def execute_trade(self):
        signal = await generate_trade_signal(self.api, "BTCUSDT", "ETHUSDT", threshold=10)
        
        if signal == "Sell BTC, Buy ETH":
            order1 = await self.api.place_order("BTCUSDT", "Sell", 0.01)
            order2 = await self.api.place_order("ETHUSDT", "Buy", 0.01)
            logging.info(f"Placed Orders: {order1}, {order2}")
            messagebox.showinfo("Trade Executed", "Sell BTC, Buy ETH Order Placed")
        elif signal == "Buy BTC, Sell ETH":
            order1 = await self.api.place_order("BTCUSDT", "Buy", 0.01)
            order2 = await self.api.place_order("ETHUSDT", "Sell", 0.01)
            logging.info(f"Placed Orders: {order1}, {order2}")
            messagebox.showinfo("Trade Executed", "Buy BTC, Sell ETH Order Placed")
        else:
            messagebox.showinfo("No Trade", "Holding Position")

# main.py
from bybit_api import BybitAPI
import tkinter as tk
from gui import TradingApp

if __name__ == "__main__":
    API_KEY = "your_api_key"
    API_SECRET = "your_api_secret"
    
    bybit = BybitAPI(API_KEY, API_SECRET)
    root = tk.Tk()
    app = TradingApp(root, bybit)
    root.mainloop()
