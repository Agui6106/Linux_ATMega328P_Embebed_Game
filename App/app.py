from tkinter import BOTH
from tkinter import Button
from tkinter import Frame
from tkinter import Label
from tkinter import messagebox
from tkinter import Tk
from tkinter import Canvas
from tkinter import PhotoImage

import subprocess
import os

from tkinter.ttk import Combobox

from utils import find_available_serial_ports
from serial_sensor import BAUDRATES
from serial_sensor import SerialSensor

# List of avaiblae games
GAMES = ['1945', 'Aseivo', 'Control Test' ]

class App(Frame):
    def __init__(self, parent, *args, **kwargs):       
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent:Tk = parent
        
        # - Eleemntos graficos juegos - #
        self.creators_names_label: Label = self._create_creators_names_label()
        # Section 1 - Game select
        self.play_button: Button = self._Create_play_button()
        self.avaibale_games: Combobox = self._create_games_combobox()
        # Section 2 - Button Interface
        self.scores_butt: Button = self._create_scores_button()
        self.UPScores_butt: Button = self._create_UP_scores_button()
        self.settings_butt: Button = self._create_Settings_button()
        self.credtis_butt: Button = self._create_Credits_button()
        
        self.init_gui()

    def init_gui(self,)-> None:
        # -- Propiedades de ventana -- #
        # Dimensiones de la pantalla 
        window_width = 500
        window_height = 600
        # Obtenemos las dimesiones de la pantalla
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Buscamos el punto medio
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.parent.title('GameNest by GameSystems Inc. - V1.0')
        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        #self.resizable(False, False)
        
        # Crear un Canvas para la imagen de fondo
        self.canvas = Canvas(self.parent, width=500, height=10)
        self.canvas.pack(expand=True, fill=BOTH)

        # Cargar y mostrar la imagen de fondo
        self.bg_image = PhotoImage(file="GameNest_Banner.png", width=500, height=100)  # Guardar referencia a la imagen
        self.canvas.create_image(0, 0, anchor='nw', image=self.bg_image) # (x,y)

        self['bg'] = ''
        self.pack(expand=True, fill=BOTH)
        
        # - Creacion de Frame de ajsutes (Section 3) - #
        self.main_frame  = Frame(master=self.parent, width=500, height=500, bg='')
        self.main_frame.pack(side='top', fill=BOTH, expand=True)

        # Centro de control
        self.frame_scores = FrameOne(self.main_frame)
        self.frame_settings = FrameTwo(self.main_frame)
        self.frame_UP_Scores = FrameThree(self.main_frame)
        self.frame_Credits = FrameFour(self.main_frame)

        # Inicialmente mostrar solo FrameOne (Scores)
        self.frame_scores.pack(fill="both", expand=True)
        
        # - Ubicacion de elementos graficos - #
        # Game select - Section 1
        self.avaibale_games.grid(row=1, column=0, sticky="n", columnspan=2, padx=20)
        self.play_button.grid(row=2, column=0, sticky= "n", columnspan=2, padx=20, pady= 10)
        
        # App Control - Section 2
        self.scores_butt.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.UPScores_butt.grid(row=3 ,column=1, sticky="w")
        self.settings_butt.grid(row=4, column=0, sticky="w", padx=10, pady=10)
        self.credtis_butt.grid(row=4 ,column=1, sticky="w")

        #self.creators_names_label.grid(row=6, column=0, columnspan=2, sticky="w")
            
    # - Juegos - #
    # Operativo - Seleccion de juego 
    def play(self) -> None:
        selected_value = self.avaibale_games.get()
        if (selected_value == "1945"):
            subprocess.run(["python3", "./1945/game.py"])
        
        if (selected_value == "Control Test"):
            subprocess.run(["python3", "control_test.py"])
            
        
    
    # Visual - Boton seleccion del juego    
    def _Create_play_button(self) -> Button:
        return Button(
            master=self,
            text = 'Play',
            font=("Z003",15,"bold"),
            command=self.play
        )
    
    # Visual - seleccionar el juego que deseamos
    def _create_games_combobox(self) -> Combobox:
        games_vals = ['Select a game'] + GAMES 
        return Combobox(
            master = self,
            values = games_vals,
            width=30,
            state="readonly",
            cursor='star',            
            font=("C059", 15), 
            justify=("center"),  
        )
        
    # Visual - Boton Scores
    def _create_scores_button(self) -> Button:
        return Button(
            master = self,
            text = 'Scores',
            command = self.show_frame_scores,
            width=20,
            cursor='spider',
            font=("Z003",15,"bold")
        )
    
    # Operativo - Cambio al Frame scores
    def show_frame_scores(self):
        self.frame_scores.pack_forget()
        self.frame_scores.pack(fill="both", expand=True)
        self.frame_settings.pack_forget()
        self.frame_Credits.pack_forget()
        self.frame_UP_Scores.pack_forget()
    
    # Visual - Upload Scores
    def _create_UP_scores_button(self) -> Button:
        return Button(
            master = self,
            text = 'Upload Scores',
            command = self.show_frame_UP_Scores,
            width=20,
            cursor='spider',
            justify='center',
            font=("Z003",15,"bold")
        )
    
    # Operativo - Cambio al Frame de UP Socres
    def show_frame_UP_Scores(self):
        self.frame_UP_Scores.pack_forget()
        self.frame_UP_Scores.pack(fill="both", expand=True)
        self.frame_settings.pack_forget()
        self.frame_Credits.pack_forget()
        self.frame_scores.pack_forget()
    
    # Visual - Local Settings
    def _create_Settings_button(self) -> Button:
        return Button(
            master = self,
            text = 'Settings',
            command = self.show_settings_frame,
            width=20,
            cursor='spider',
            font=("Z003",15,"bold")
        )
    
    # Operativo - Cambio al Frame scores
    def show_settings_frame(self):
        self.frame_settings.pack_forget()
        self.frame_settings.pack(fill="both", expand=True)
        self.frame_scores.pack_forget()
        self.frame_Credits.pack_forget()
        self.frame_UP_Scores.pack_forget()
    
    # Visual - Credits
    def _create_Credits_button(self) -> Button:
        return Button(
            master = self,
            text = 'Credits',
            command = self.show_frame_Credits,
            width=20,
            cursor='spider',
            font=("Z003",15,"bold")
        )
    
    # Operativo - Cambio al Frame de UP Socres
    def show_frame_Credits(self):
        self.frame_Credits.pack_forget()
        self.frame_Credits.pack(fill="both", expand=True)
        self.frame_settings.pack_forget()
        self.frame_UP_Scores.pack_forget()
        self.frame_scores.pack_forget()
    
    # US
    def _create_creators_names_label(self) -> Label:
        return Label(
            master = self,
            text = 'With love: Paulina, Israel, Aguilar',
            background='black',
            foreground = 'white',
            font=("Courier", 10),
            cursor='heart'
        )
        
# -- Frames de control (Section 3)-- #
# Scores Frame
class FrameOne(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Ejemplo de contenido para FrameOne
        Label(self, text="This is scores Frame").pack()

# Settings Frame
class FrameTwo(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent: Tk = parent
        # Esta variable puede ser del tipo sensor o nada
        self.serial_device: SerialSensor | None = None
        #  Creacion de elementos graficos
        self.serial_devices_combobox: Combobox = self._init_serial_devices_combobox()
        self.refresh_serial_devices_button: Button = self._create_refresh_serial_devices_button()
        self.baudrate_combobox: Combobox = self._create_baudrate_combobox()
        self.connet_button: Button = self._create_connect_button()
        self.title_label: Label = self._create_Settings_label()
        #self.temperature_label: Label = self._create_temperature_label()
        #self.read_temperature_button: Button = self._create_temperature_button()
        
        self.init_gui()
    
    def init_gui(self,) -> None:
        self.title_label.grid(row=0, column=0, columnspan=2, sticky ='n',padx=40)
        self.serial_devices_combobox.grid(row=1, column=0, columnspan= 2,  padx=40)
        self.baudrate_combobox.grid(row = 2, column = 0, columnspan= 2, padx=40, pady= 10)
        self.refresh_serial_devices_button.grid(row = 3, column = 0,padx=20)
        self.connet_button.grid(row = 3, column = 1)
        
        # Others Settings
        self.baudrate_combobox.current(0) # No esta seleccionado
    
    # - Titulo - #
    def _create_Settings_label(self) -> Label:
        return Label(
            master = self,
            text = 'Settings',
            foreground = 'black',
            font=("Z003",20,"bold")
        )
        
    # -- Dispositvo serial -- #
    # Visual - seleccion de puertos
    def _init_serial_devices_combobox(self, ) -> Combobox:
        ports = ['Select a serial port'] + find_available_serial_ports()
        return Combobox(
            self, 
            values=ports, 
            font=("Courier", 15), 
            state="readonly",
            width=30, 
            cursor='trek'
        )
    
    # Operativo - seleccion de puertos
    def refresh_serial_devices(self) -> None:
        ports = find_available_serial_ports()
        self.serial_devices_combobox['values'] = ports
    
    # Visual - buscar dispostivos seriales
    def _create_refresh_serial_devices_button(self,) -> Button:
        return Button(
            master = self,
            text = "Refresh serial devices",
            cursor='exchange',
            width=20,
            font=("Helvetica",12,"bold"),
            command = self.refresh_serial_devices
        )
    
    # Visual - seleccionar baudrates
    def _create_baudrate_combobox(self) -> Combobox:
        baudrates_values = ['BAUDRATE'] + BAUDRATES
        return Combobox(
            master = self,
            values = baudrates_values,
            width=30,
            cursor='star',
            state="readonly"
        )
    
    # Operativo - Conexion al puerto serial
    def connect_serial_device(self) -> None:
        try:        
            baudrate = int(self.baudrate_combobox.get())
            port = self.serial_devices_combobox.get()
            if port == '':
                 messagebox.showerror('Port not selected',f'Select a valid port {port =}')
            self.serial_device = SerialSensor(
                port = port,
                baudrate = baudrate
            ) 
                
        except ValueError:
            messagebox.showerror('Wrong baudrate','Baudrate not valid')
            return
    
    # Visual - Conexion al puerto serial    
    def _create_connect_button(self,) -> Button:
        return Button(
            master = self,
            text = 'Connect',
            command = self.connect_serial_device,
            width=20,
            cursor='spider',
            font=("Helvetica",12,"bold")
        ) 

    # Operativo - Lectura de serial 
    def read_serial(self) -> None:
        if self.serial_device is not None:
            temperature = self.serial_device.send('TC2')
            self.temperature_label['text'] = f"{temperature[1:-4]} C"
            return
        messagebox.showerror(title='Serial connection error', message='Serial device not initializate')
    

# UP Socres frame
class FrameThree(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Ejemplo de contenido para FrameTwo
        Label(self, text="This is Upload Scores Frame").pack()
     
# Credits Frame   
class FrameFour(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Ejemplo de contenido para FrameTwo
        Label(self, text="This is credits Frame").pack()
        
# ------------------------------------------------------ #

root = Tk()

if __name__ == '__main__':
    ex = App(root)
    root.mainloop()