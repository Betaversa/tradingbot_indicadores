import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
import time

# URL de la Testnet de Binance
BASE_URL = 'https://testnet.binance.vision/api'

# Tus claves de prueba
API_KEY = 'g9kfa67zCF8yBQ2SekK95BpQn9JOuH4a14qwRwf2BdsXSopcz5uIIs6ENqV8ypMf'
API_SECRET = 'NvDmatyVBF0lKkTJ2fqimR6UD3Hwp922dPaHaXJCoToTYIMedZZIEOJNHaSUJcv1'

# Conexión al cliente con la testnet
client = Client(API_KEY, API_SECRET)
client.API_URL = BASE_URL

# Prueba de conexión
try:
    status = client.ping()
    print("✅ Conexión exitosa con Binance Testnet:", status)

    # Aquí puedes poner tu lógica de trading, por ejemplo:
    # precios = client.get_symbol_ticker(symbol="BTCUSDT")
    # print("Precio BTCUSDT:", precios)

except BinanceAPIException as e:
    print("❌ Error al conectar con Binance:", e)
