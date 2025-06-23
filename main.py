import os
import time
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Configuración de logging para debug
logging.basicConfig(level=logging.INFO)

# 🚀 Claves de API desde las variables de entorno
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# 🔁 Usar la URL del entorno de PRUEBAS de Binance
BASE_URL = 'https://testnet.binance.vision/api'

# Instanciar cliente Binance apuntando a TESTNET
client = Client(API_KEY, API_SECRET)
client.API_URL = BASE_URL

# 📊 Parámetros del bot
SYMBOL = 'BTCUSDT'
INTERVAL = '1m'
LIMIT = 20

def get_price():
    try:
        ticker = client.get_symbol_ticker(symbol=SYMBOL)
        price = float(ticker['price'])
        logging.info(f"💰 Precio actual de {SYMBOL}: {price}")
        return price
    except BinanceAPIException as e:
        logging.error(f"❌ Error API Binance: {e}")
        return None

def main_loop():
    logging.info("🚀 Iniciando Trading Bot en Testnet...")
    while True:
        price = get_price()
        # Aquí podrías aplicar lógica con RSI, EMA, etc.
        time.sleep(60)  # Espera 60 segundos entre consultas

if __name__ == "__main__":
    main_loop()
