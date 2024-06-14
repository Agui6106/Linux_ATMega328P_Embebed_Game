"""

# --  TKinter with Pygame -- #
import tkinter as tk  # Import the Tkinter library
import pygame  # Import the Pygame library

# Creating the Tkinter Form
def get_input():
   # Retrieve user input from Tkinter entry widget
   user_input = entry.get()
   # Initialize Pygame with the user input
   pygame_init(user_input)

# Initializing Pygame with Input
def pygame_init(user_input):
   pygame.init()
   # Use the user_input in your Pygame code as needed
   print("Input from form:", user_input)
   pygame.quit()

# Running the Application
if __name__ == "__main__":
   # Create Tkinter window
   root = tk.Tk()  # Create the main Tkinter window
   root.title("Form Input using Tkinter in Pygame")  
   root.geometry("720x250")

   # Create Tkinter label
   label = tk.Label(root, text="Enter your input:")  
   label.pack(pady=15)  

   # Create Tkinter entry widget
   entry = tk.Entry(root)  
   entry.pack(pady=10)

   # Create Tkinter button with the get_input function 
   button = tk.Button(root, text="Submit", command=get_input)  
   button.pack(pady=10)  

   # Run the Tkinter main loop
   root.mainloop()  

   
# -- List of fotns in tkinter -- #
#Import required library
from tkinter import *
from tkinter import font
#Create an instance of tkinter frame
win = Tk()
win.geometry("750x350")
win.title('Font List')
#Create a list of font using the font-family constructor
fonts=list(font.families())
fonts.sort()
def fill_frame(frame):
   for f in fonts:
      #Create a label to display the font
      label = Label(frame,text=f,font=(f, 14)).pack()
def onFrameConfigure(canvas):
   canvas.configure(scrollregion=canvas.bbox("all"))
#Create a canvas
canvas = Canvas(win,bd=1, background="white")
#Create a frame inside the canvas
frame = Frame(canvas, background="white")
#Add a scrollbar
scroll_y = Scrollbar(win, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll_y.set)
scroll_y.pack(side="right", fill="y")
canvas.pack(side="left", expand=1, fill="both")
canvas.create_window((5,4), window=frame, anchor="n")
frame.bind("<Configure>", lambda e, canvas=canvas: onFrameConfigure(canvas))
fill_frame(frame)
win.mainloop()

# -- 2 frames ant the same time -- #
import tkinter as tk
from tkinter import ttk

class FrameOne(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.init_ui()

    def init_ui(self):
        label = tk.Label(self, text="This is Frame One", font=("Arial", 16))
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Combobox that spans two columns
        self.available_games = ttk.Combobox(self, values=["Game 1", "Game 2", "Game 3"])
        self.available_games.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        button = tk.Button(self, text="Click me in Frame One", command=self.on_button_click)
        button.grid(row=2, column=0, columnspan=2, pady=10)

    def on_button_click(self):
        print("Button in Frame One clicked")

class FrameTwo(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.init_ui()

    def init_ui(self):
        label = tk.Label(self, text="This is Frame Two", font=("Arial", 16))
        label.grid(row=0, column=0, padx=10, pady=10)

        button = tk.Button(self, text="Click me in Frame Two", command=self.on_button_click)
        button.grid(row=1, column=0, pady=10)

    def on_button_click(self):
        print("Button in Frame Two clicked")

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Multi-Frame Application")
        self.geometry("600x400")

        # Create a main frame to hold both FrameOne and FrameTwo
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Create and place FrameOne in the left side of the main frame
        frame_one = FrameOne(main_frame)
        frame_one.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Create and place FrameTwo in the right side of the main frame
        frame_two = FrameTwo(main_frame)
        frame_two.pack(side="right", fill="both", expand=True, padx=10, pady=10)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

# -- Cambio entre 2 frames -- #
import tkinter as tk
from tkinter import ttk

class FrameOne(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.init_ui()

    def init_ui(self):
        label = tk.Label(self, text="This is Frame One", font=("Arial", 16))
        label.pack(padx=10, pady=10)
        
        button = tk.Button(self, text="Switch to Frame Two", command=self.switch_to_frame_two)
        button.pack(pady=10)
    
    def switch_to_frame_two(self):
        self.master.switch_frame(FrameTwo)

class FrameTwo(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.init_ui()

    def init_ui(self):
        label = tk.Label(self, text="This is Frame Two", font=("Arial", 16))
        label.pack(padx=10, pady=10)
        
        button = tk.Button(self, text="Switch to Frame One", command=self.switch_to_frame_one)
        button.pack(pady=10)
    
    def switch_to_frame_one(self):
        self.master.switch_frame(FrameOne)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Multi-Frame Application")
        self.geometry("400x300")
        
        self._frame = None
        self.switch_frame(FrameOne)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
    """
"""
# -- Bluethoot test -- #
import serial
import time

# Configurar el puerto serial
port = serial.Serial("/dev/rfcomm0", baudrate=2400)

# Lectura de datos del puerto serial
try:
    while True:
        print("DIGITAL LOGIC -- > READING...")
        recieved = serial.readline()
        print(recieved)
        time.sleep(3)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    port.close()

"""

# - Pygame and Pyseria - #       
import pygame
import serial
import sys

# Configuración del puerto serial
ser = serial.Serial(
    port='/dev/ttyUSB0',  # Reemplaza con el nombre de tu puerto
    baudrate=9600,
    timeout=1
)

# Inicializar Pygame
pygame.init()

# Establecer dimensiones de la pantalla
screen = pygame.display.set_mode((800, 600))

# Título de la ventana
pygame.display.set_caption('Control de Pygame con PySerial')

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
input_box = pygame.Rect(100, 100, 140, 32)
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

"""
    # -- PyGame Control test
class PygameApp:
    def __init__(self, serial_device):
        pygame.init()
        pygame.display.set_caption("Control Test")
        self.resolution = (500, 500)
        self.screen = pygame.display.set_mode(self.resolution, 0, 32)
        self.clock = pygame.time.Clock()
        self.serial_device: SerialSensor | None = None
    
    # Fuente para la caja de texto
    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    
    # Función para leer datos del puerto serial
    def read_serial():
        if self.serial_device.in_waiting > 0:
            try:
                data = ser.readline().decode().strip()
                return data
            except:
                return None
        return None
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.screen.fill((0, 0, 0))

            # Aquí puedes agregar el código para leer del puerto serial y dibujar en la pantalla
            if self.serial_device:
                try:
                    # Enviar un comando y recibir respuesta
                    sent_command = "your_command_here: "
                    response = self.serial_device.send(sent_command)
                    print(f"Respuesta recibida: {response}")

                    # Recibir datos continuamente
                    received_data = self.serial_device.reception()
                    if received_data:
                        print(f"Datos recibidos: {received_data}")

                    # Agrega aquí el código para manejar los datos recibidos y dibujar en la pantalla
                except SerialException as e:
                    print(f"Error leyendo del dispositivo serial: {e}")
                    self.serial_device = None  # Desconecta el dispositivo si hay un error

            pygame.display.update()
            self.clock.tick(30)  # Limita la velocidad de fotogramas a 30 FPS

        pygame.quit()
"""