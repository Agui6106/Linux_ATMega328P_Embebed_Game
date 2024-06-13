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

# Fuente para escribir un texto
font = pygame.font.Font(None, 32)
input_box = pygame.Rect(20, 50, 700, 32)
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

# Función para mostrar el texto recibido del puerto serial
def display_serial_text(screen, font, text, position):
    if text:
        serial_disp_txt = font.render(text, True, BLUE)
        screen.blit(serial_disp_txt, position)

# Solicitar un comando. Mostrar texto
text_surface = font.render("Input a command:", True, WHITE)

# Texto recibido. Mostar texto fijo
recv_txt = font.render("Response:", True, WHITE)

# Lo que recibi. Texto variable por la lectura serial
serial_text = read_serial()
serial_disp_txt = font.render(serial_text, True, BLUE)

# - Reaccion a botones - #
# Start
strt_text_surface = font.render("Start Button", True, WHITE)
show_start_text = False  # Variable de estado para controlar la visibilidad del tstrt
# Escape
escape_text_surface = font.render("Escape Button", True, WHITE)
show_escape_text = False  # Variable de estado para controlar la visibilidad del texto
# Jump
jump_text_surface = font.render("Jump Button", True, WHITE)
show_jump_text = False  # Variable de estado para controlar la visibilidad del texto
# Shoot
shoot_text_surface = font.render("Shoot Button", True, WHITE)
show_shoot_text = False  # Variable de estado para controlar la visibilidad del texto

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
            
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    ser.write(text.encode())
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    
    # Rellenar la pantalla con negro
    screen.fill(BLACK)

    # Dibujar el círculo
    pygame.draw.circle(screen, WHITE, (x, y), radius)

    # Renderizar el texto de entrada
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)

    # - Mostrar texto en la pantalla - #
    # Input a command:
    screen.blit(text_surface, (20, 20))
    # Response:
    screen.blit(recv_txt, (500, 20))
    # Leer y mostrar datos del puerto serial
    command = read_serial()
    display_serial_text(screen, font, command, (500, 50))
    
    # Reaccion a botones
    if show_start_text:
        screen.blit(strt_text_surface, (20, 100))
    if show_escape_text:
        screen.blit(escape_text_surface, (20, 200))
    if show_jump_text:
        screen.blit(jump_text_surface, (20, 300)) 
    if show_shoot_text:
        screen.blit(shoot_text_surface, (20, 400))
    # Actualizar la pantalla
    pygame.display.flip()

    # - Reaccionamos a la input recibida - #
    if command:
        # Inputs Joystick
        if command == 'I':
            x -= speed
        elif command == 'D':
            x += speed
        elif command == 'A':
            y -= speed
        elif command == 'a':
            y += speed
        # Inputs Botones
        elif command == 'Str':
            show_start_text = True
            show_escape_text = False
            show_jump_text = False
            show_shoot_text = False
        elif command == 'Esc':
            show_start_text = False
            show_escape_text = True
            show_jump_text = False
            show_shoot_text = False
        elif command == 'Jmp':
            show_start_text = False
            show_escape_text = False
            show_jump_text = True
            show_shoot_text = False
        elif command == 'Sho':
            show_start_text = False
            show_escape_text = False
            show_jump_text = False
            show_shoot_text = True
            
    """
        Received command list:
        - Movement
            Izquierda = I
            Derecha = D
            Arriba = A
            Abajo = a
            
        - Acciones
            Start On = str
            Escape On = esc
            Jump On = jmp
            Shoot On = sho
            
            Start Off = st0
            Escape Off = es0
            Jump Off = jm0
            Shoot Off = sh0
        
        Sent command list:
    """
    
    # Controlar la velocidad del bucle
    pygame.time.Clock().tick(60)

# Cerrar el puerto serial
ser.close()

# Salir de Pygame
pygame.quit()
sys.exit()
