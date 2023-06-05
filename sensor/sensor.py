import time
import Adafruit_DHT

# Tipo de sensor
sensor = Adafruit_DHT.DHT11  # DHT11

# Pin al que está conectado el sensor
pin = 5  # D5

def read_humidity_temp_sensor():
    try:
        # Leer datos del sensor de humedad y temperatura
        humidity, temp = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temp is not None:
            return humidity, temp
        else:
            return None, None
    except IOError as e:
        print("Error al leer el sensor de humedad y temperatura:", str(e))
        return None, None
    except TypeError as e:
        print("Error de tipo de dato al leer el sensor de humedad y temperatura:", str(e))
        return None, None

