# - Pygame and Pyseria - #       
import pygame
import serial
import sys

# Verifcamos herecnia de componentes
if len(sys.argv) != 3:
    print("Usage: python pygame_script.py <port> <baudrate>")
    sys.exit(1)

port = sys.argv[1]
baudrate = int(sys.argv[2])

# Configuración del puerto serial
ser = serial.Serial(
    port=port,  # Reemplaza con el nombre de tu puerto
    baudrate=baudrate,
    timeout=1
)

# Inicializar Pygame
pygame.init()

# Establecer dimensiones de la pantalla
screen = pygame.display.set_mode((800, 600))

# Título de la ventana
pygame.display.set_caption('Control Test')

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Posición inicial del círculo
x, y = 400, 300
radius = 30
speed = 5

# Fuente para la caja de texto
font = pygame.font.Font(None, 32)
input_box = pygame.Rect(100, 500, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''

# Función para leer datos del puerto serial
def read_serial():
    if ser.in_waiting > 0:
        try:
            data = ser.readline().decode().strip()
            return data
        except:
            return None
    return None

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el usuario hace clic en la caja de texto
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    # Enviar el texto por el puerto serial
                    ser.write(text.encode())
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    # Leer datos del puerto serial
    command = read_serial()
    if command:
        if command == 'LEFT':
            x -= speed
        elif command == 'RIGHT':
            x += speed
        elif command == 'UP':
            y -= speed
        elif command == 'DOWN':
            y += speed

    # Limpiar la pantalla
    screen.fill(BLACK)

    # Dibujar el círculo
    pygame.draw.circle(screen, WHITE, (x, y), radius)

    # Renderizar el texto
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del bucle
    pygame.time.Clock().tick(60)

# Cerrar el puerto serial
ser.close()

# Salir de Pygame
pygame.quit()
sys.exit()
