from tkinter import BOTH
from tkinter import Button
from tkinter import Frame
from tkinter import Label
from tkinter import messagebox
from tkinter import Tk

import subprocess
import pygame

from tkinter.ttk import Combobox

from utils import find_available_serial_ports
from serial_sensor import BAUDRATES
from serial_sensor import SerialSensor

class App(Frame):

    def __init__(self, parent, *args, **kwargs):       
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent:Tk = parent
        # Esta variable puede ser del tipo sensor o nada
        self.serial_device: SerialSensor | None = None
        # Aqui vamos a crear todos los componentes graficos
        self.serial_devices_combobox: Combobox = self._init_serial_devices_combobox()
        self.refresh_serial_devices_button: Button = self._create_refresh_serial_devices_button()
        self.baudrate_combobox: Combobox = self._create_baudrate_combobox()
        self.connet_button: Button = self._create_connect_button()
        self.temperature_label: Label = self._create_temperature_label()
        self.read_temperature_button: Button = self._create_temperature_button()
        self.creators_names_label: Label = self._create_creators_names_label()
        self.draw_button: Button = self._Create_draw_button()
        self.init_gui()
        """
        resolution = (320, 480)
        screen = pygame.display.set_mode((resolution))
        screen.fill(pygame.Color(255,255,255))
        self.screen = screen
        pygame.display.init()
        pygame.display.update()  

        """
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
        self.parent.title('GameNest- V1.0')
        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self['bg'] = ''
        self.pack(expand=True, fill=BOTH)

        # Ubicacion de elementos graficos #

        #row 0
        
        self.serial_devices_combobox.grid(row=1, column=0, padx=20, pady=30)
        self.refresh_serial_devices_button.grid(row = 1, column = 1, pady= 30)
        self.baudrate_combobox.grid(row = 2, column = 0)
        self.connet_button.grid(row = 2, column = 1)
        
        self.draw_button.grid(row=3, column=0)
        #row 1
        
        self.temperature_label.grid(row = 4, column = 0, pady=30)
        self.read_temperature_button.grid(row = 4, column = 1, pady=30)
        self.creators_names_label.grid(row=5, column=0 )
        
        #other settings
        self.baudrate_combobox.current(0) # No esta seleccionado
    
    # -- Dispositvo serial -- #
    # Visual - seleccion de puertos
    def _init_serial_devices_combobox(self, ) -> Combobox:
        ports = ['Select a serial port'] + find_available_serial_ports()
        return Combobox(
            self, 
            values=ports, 
            font=("Courier", 20), 
            width=15, 
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
            command = self.refresh_serial_devices
        )
    
    # Visual - seleccionar baudrates
    def _create_baudrate_combobox(self) -> Combobox:
        baudrates_values = ['BAUDRATE'] + BAUDRATES
        return Combobox(
            master = self,
            values = baudrates_values,
            width=30,
            cursor='star'
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
            width=18,
            cursor='spider',
            font=("Helvetica",11,"bold")
        )
    
    # Visual - Despliege de temperatura
    def _create_temperature_label(self) -> Label:
        return Label(
            master = self,
            text = 'XX.X °C',
            background='black',
            foreground = 'white',
            font=("monospace",20,"italic")
        )
    
    # Operativo - Boton de despliege de temperatura    
    def _create_temperature_button(self) -> None:
        return Button(
            master = self,
            text = 'Read temperature',
            command = self.read_temperature,
            width=18,
            cursor='watch'
        )
        
    # Operativo - Lectura de temperaturas 
    def read_temperature(self) -> None:
        if self.serial_device is not None:
            temperature = self.serial_device.send('TC2')
            self.temperature_label['text'] = f"{temperature[1:-4]} C"
            return
        messagebox.showerror(title='Serial connection error', message='Serial device not initializate')
            
    
    def draw(self) -> None:
        subprocess.run(["python3", "/home/ingesitos/Documents/1945/game.py"])
        
    def _Create_draw_button(self) -> Button:
        return Button(
            master=self,
            text = 'Draw',
            command=self.draw
        )
    
    
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
        

root = Tk()

if __name__ == '__main__':
    ex = App(root)
    root.mainloop()