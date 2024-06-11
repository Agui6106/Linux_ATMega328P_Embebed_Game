import serial
import time
from app import FrameTwo

def read_serial(port='/dev/ttyS0', baudrate=9600, timeout=1):
    try:
        # Configurar el puerto serial
        ser = serial.Serial(port, baudrate, timeout=timeout)
        print(f"Conectado al puerto {port} a {baudrate} baudios.")

        # Leer datos continuamente
        while True:
            if ser.in_waiting > 0:
                # Leer una línea del puerto serial
                line = ser.readline().decode('utf-8').rstrip()
                print(f"Datos recibidos: {line}")

            time.sleep(1)  # Esperar un segundo antes de leer de nuevo
    except serial.SerialException as e:
        print(f"Error al conectar al puerto serial: {e}")
    except KeyboardInterrupt:
        print("Lectura interrumpida por el usuario.")
    finally:
        # Cerrar el puerto serial
        if ser.is_open:
            ser.close()
            print("Puerto serial cerrado.")

if __name__ == "__main__":
    # Llama a la función para leer datos del puerto serial
    read_serial()
