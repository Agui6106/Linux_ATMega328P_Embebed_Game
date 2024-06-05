## Encontrar los puertos seriales disponibles
# -- Encontrar los puertos seriales disponibles -- #
import serial.tools.list_ports

def find_ports() -> list[str]:
    ports = serial.tools.list_ports.comports()
    serial_ports = []
    for port in ports:
        serial_ports.append(port.device)
    return serial_ports

if __name__ == "_main_":
    print("Puertos seriales disponibles:")
    ports = find_ports()
    for port in ports:
        print(port)