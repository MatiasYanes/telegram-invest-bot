import yfinance as yf
import requests
from datetime import datetime
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


STOCKS = {
    "NVDA": {"buy_drop": -5, "sell_gain": 25},
    "GOOGL": {"buy_drop": -6, "sell_gain": 20},
    "AMZN": {"buy_drop": -5, "sell_gain": 20},
    "AMD": {"buy_drop": -7, "sell_gain": 25},
    "SOFI": {"buy_drop": -10, "sell_gain": 30},
    "NU": {"buy_drop": -8, "sell_gain": 30},
    "VIST": {"buy_drop": -10, "sell_gain": 35},
}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def check_stocks():
    for symbol, rules in STOCKS.items():
        data = yf.Ticker(symbol).history(period="5d")

        if len(data) < 2:
            continue

        prev = data["Close"][-2]
        last = data["Close"][-1]
        change = ((last - prev) / prev) * 100

        if change <= rules["buy_drop"]:
            send_telegram(
                f"📉 OPORTUNIDAD DE COMPRA\n"
                f"{symbol} cayó {change:.2f}%\n"
                f"Precio: {last:.2f} USD"
            )

        if change >= rules["sell_gain"]:
            send_telegram(
                f"📈 TAKE PROFIT\n"
                f"{symbol} subió {change:.2f}%\n"
                f"Considerar venta parcial"
            )

if __name__ == "__main__":
    check_stocks()
