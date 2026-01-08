import yfinance as yf
import requests
from datetime import datetime
import os

# =========================
# CONFIGURACIÓN TELEGRAM
# =========================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# ACTIVOS Y REGLAS
# =========================
STOCKS = {
    "NVDA": {"buy_drop": -5, "sell_gain": 25},
    "GOOGL": {"buy_drop": -6, "sell_gain": 20},
    "AMZN": {"buy_drop": -5, "sell_gain": 20},
    "AMD": {"buy_drop": -7, "sell_gain": 25},
    "SOFI": {"buy_drop": -10, "sell_gain": 30},
    "NU": {"buy_drop": -8, "sell_gain": 30},
    "VIST": {"buy_drop": -10, "sell_gain": 35},
}

# =========================
# ENVÍO A TELEGRAM
# =========================
def send_telegram(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Error: TELEGRAM_TOKEN o CHAT_ID no configurados")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

# =========================
# SNAPSHOT DE PRECIOS
# =========================
def send_prices_snapshot():
    message = "📊 PRECIOS ACTUALES\n\n"

    for symbol in STOCKS.keys():
        try:
            price = yf.Ticker(symbol).fast_info["last_price"]
            if price is None:
                raise ValueError("Precio no disponible")
            message += f"{symbol}: {price:.2f} USD\n"
        except Exception:
            message += f"{symbol}: precio no disponible\n"

    send_telegram(message)

# =========================
# ALERTAS DIARIAS
# =========================
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

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    send_prices_snapshot()   # mensaje de prueba
    check_stocks()           # alertas normales
