import time
import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os

# Variables de entorno (Render → Environment)
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

client = Client(API_KEY, API_SECRET)

SYMBOL = "BTCUSDT"
INTERVAL = Client.KLINE_INTERVAL_1MINUTE
LIMIT = 100

def get_klines():
    try:
        klines = client.get_klines(symbol=SYMBOL, interval=INTERVAL, limit=LIMIT)
        df = pd.DataFrame(klines, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])
        df["close"] = df["close"].astype(float)
        return df
    except BinanceAPIException as e:
        print("Error al obtener datos:", e)
        return None

def calculate_indicators(df):
    df["EMA20"] = df["close"].ewm(span=20).mean()
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    return df

def trading_logic(df):
    last_row = df.iloc[-1]
    if last_row["RSI"] < 30 and last_row["close"] > last_row["EMA20"]:
        print("📈 Señal de COMPRA detectada.")
        # client.order_market_buy(symbol=SYMBOL, quantity=0.001)
    elif last_row["RSI"] > 70 and last_row["close"] < last_row["EMA20"]:
        print("📉 Señal de VENTA detectada.")
        # client.order_market_sell(symbol=SYMBOL, quantity=0.001)
    else:
        print("⏳ Sin señales claras.")

if __name__ == "__main__":
    print("🔄 TradingBot corriendo...")
    while True:
        df = get_klines()
        if df is not None:
            df = calculate_indicators(df)
            trading_logic(df)
        time.sleep(10)
