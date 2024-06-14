from tkinter import BOTH
from tkinter import Button
from tkinter import Frame
from tkinter import Label
from tkinter import messagebox
from tkinter import Tk
from tkinter import Canvas
from tkinter import PhotoImage
from tkinter import Text

import subprocess
import socket
import threading
import os
import signal
import webbrowser

from tkinter.ttk import Combobox

from utils import find_available_serial_ports
from serial_sensor import BAUDRATES
from serial_sensor import SerialSensor

# List of avaiblae games
GAMES = ['1945', 'Aseivo', 'PyDOOM' ,'Control Test' ]

Global_Scores =0

# - Inicialziacion del server Socket - #
class GameServer:
    
    # Configruacion de aprametros del server
    def __init__(self, host='0.0.0.0', port=3333):
        self.host = host
        self.port = port
        self.high_score = Global_Scores
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
    
    # Inicializar servidor
    def start(self):
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"New connection from {client_address}")
                # Manage each client in a separate thread
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.server_socket.close()
            
    # Comunicacion con el cliente
    def handle_client(self, client_socket, client_address):
        self.clients.append(client_socket)
        while True:
            try:
                message = client_socket.recv(1024)
                if not message:
                    break
                self.high_score = message.decode('utf-8')
                Global_Scores = self.high_score
                print(f"Received message from {client_address}: {self.high_score}")
                print(f" HS: {Global_Scores}")
                self.broadcast_message(self.high_score, client_socket)
                        
            except Exception as e:
                print(f"Error with client {client_address}: {e}")
            finally:
                print(f"Closing connection with {client_address}")
                self.clients.remove(client_socket)
                client_socket.close()


    def broadcast_message(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:  # Avoid sending the message back to the sender
                try:
                    client.sendall(message)
                except Exception as e:
                    print(f"Failed to send message to a client: {e}")
                    
    def get_high_score(self):
        print(f"{Global_Scores}")
        return Global_Scores

# - Aplicacion Prinicapal - #
class App(Frame):
    def __init__(self, parent, *args, **kwargs):       
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent:Tk = parent
        
        # Variable GLOBAL lecutrua del serial
        self.serial_device: SerialSensor | None = None
        
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
        self.frame_Credits = FrameFour(self.main_frame)

        # Inicialmente mostrar solo FrameOne (Scores)
        self.frame_settings.pack(fill="both", expand=True)
        
        # - Ubicacion de elementos graficos - #
        # Game select - Section 1
        self.avaibale_games.grid(row=1, column=0,columnspan=2, padx=20)
        self.play_button.grid(row=2, column=0, sticky= "n", columnspan=2, padx=20, pady= 10)
        
        # App Control - Section 2
        self.scores_butt.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.UPScores_butt.grid(row=3 ,column=1, sticky="w")
        self.settings_butt.grid(row=4, column=0, sticky="w", padx=10, pady=10)
        self.credtis_butt.grid(row=4 ,column=1, sticky="w")
            
    # - Juegos - #
    # Operativo - Seleccion de juego 
    def play(self) -> None:
        selected_value = self.avaibale_games.get()    
        baudrate = self.frame_settings.return_bauds()
        port = self.frame_settings.return_device()
        
        if (selected_value == "1945"):
            try:
                subprocess.Popen(["python3", "./1945/game.py", port, baudrate])
            except Exception as e:
                messagebox.showerror('Error', f'Failed to start game: {str(e)}')

        elif selected_value == "Aseivo":
            subprocess.run(["python3", "./aseivo.py"])
            
        elif selected_value == "PyDOOM":
            messagebox.showwarning("Warning", "PyDoom only compatible with keyboard")
            subprocess.run(["python3", "./DOOM-style-Game/main.py"])
        
        elif selected_value == "Control Test":
            subprocess.Popen(["python3", "./Control_test.py", port, baudrate])
   
    # Visual - Boton seleccion del juego    
    def _Create_play_button(self) -> Button:
        return Button(
            master=self,
            text = 'Play',
            font=("Z003",15,"bold"),
            cursor="trek",
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
            cursor='exchange',            
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
            cursor='star',
            font=("Z003",15,"bold")
        )
    
    # Operativo - Cambio al Frame scores
    def show_frame_scores(self):
        self.frame_scores.pack_forget()
        self.frame_scores.pack(fill="both", expand=True)
        self.frame_settings.pack_forget()
        self.frame_Credits.pack_forget()
    
    # Visual - Upload Scores
    def _create_UP_scores_button(self) -> Button:
        return Button(
            master = self,
            text = 'Upload Scores',
            command = self.message_Scores,
            width=20,
            cursor='spider',
            justify='center',
            font=("Z003",15,"bold")
        )
    
    # Operativo - Want to up scores?
    def message_Scores(self) -> None:
        user_response = messagebox.askokcancel(
            title="Upload Scores", 
            message="Want to upload scores to web?"
        )
        
        if user_response:
            print("User chose to upload scores")
            nav1 = webbrowser.get("firefox")
            nav1.open("http://192.168.137.29:8081")
            
        else:
            print("User chose not to upload scores")
                
    # Visual - Local Settings
    def _create_Settings_button(self) -> Button:
        return Button(
            master = self,
            text = 'Settings',
            command = self.show_settings_frame,
            width=20,
            cursor='spraycan',
            font=("Z003",15,"bold")
        )
    
    # Operativo - Cambio al Frame scores
    def show_settings_frame(self):
        self.frame_settings.pack_forget()
        self.frame_settings.pack(fill="both", expand=True)
        self.frame_scores.pack_forget()
        self.frame_Credits.pack_forget()
    
    # Visual - Credits
    def _create_Credits_button(self) -> Button:
        return Button(
            master = self,
            text = 'Credits',
            command = self.show_frame_Credits,
            width=20,
            cursor='heart',
            font=("Z003",15,"bold")
        )
    
    # Operativo - Cambio al Frame de UP Socres
    def show_frame_Credits(self):
        self.frame_Credits.pack_forget()
        self.frame_Credits.pack(fill="both", expand=True)
        self.frame_settings.pack_forget()
        self.frame_scores.pack_forget()
        
# -- Frames de control (Section 3)-- #
# Scores Frame
class FrameOne(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        # - Inicializamos los elemntos  - #
        self.title: Label = self._create_Scores_label()
        self.scores_txt: Text = self._create_scores_text()
        
        # - Escribimso los scores locales - #
        self.scores_txt.insert('1.0','                     - Actual Scores - \n')
        self.scores_txt.insert('3.0', f' 1945   - {Global_Scores}\n')
        self.scores_txt.insert('4.0',  ' Aseivo - 0000 \n')
        self.scores_txt.insert('5.0',  ' PyDoom -  N/A \n')
        
        #self.scores_txt.config(state='disabled')
        
        self.init_gui()
        
    # Inicialziamos los elemntos graficos
    def init_gui(self,) -> None:
        self.title.grid(row=0, column=0, columnspan=2,padx=40)
        self.scores_txt.grid(row=1, column=0,columnspan=2,rowspan=3, padx=5)
        
    # -- Funciones -- # 
    # - Titulo - #
    def _create_Scores_label(self) -> Label:
        return Label(
            master = self,
            text = 'Scores',
            foreground = 'black',
            font=("Z003",20,"bold")
        )
        
    # - Contenido - #
    def _create_scores_text(self) -> Text:
        return Text(
            master=self,
            width=60,
            height= 5
        )
    
# Settings Frame
class FrameTwo(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent: Tk = parent
        
        self.server_process: subprocess.Popen | None = None  # Almacena el proceso del servidor
        self.serial_device: SerialSensor | None = None
        
        #  Creacion de elementos graficos
        self.title_label: Label = self._create_Settings_label()
        self.serial_devices_combobox: Combobox = self._init_serial_devices_combobox()
        self.baudrate_combobox: Combobox = self._create_baudrate_combobox()
        self.refresh_serial_devices_button: Button = self._create_refresh_serial_devices_button()
        self.connet_button: Button = self._create_connect_button()
        self.server_launch_button: Button = self._create_server_but()
        #self.server_stop_button: Button = self._create_server_stop_but()  # Botón para detener el servidor
        
        self.init_gui()
    
    def init_gui(self,) -> None:
        # - Colocacion de elementos graficos
        self.title_label.grid(row=0, column=0, columnspan=2, sticky ='n',padx=40)
        
        self.serial_devices_combobox.grid(row=1, column=0, columnspan= 2,  padx=40)
        self.baudrate_combobox.grid(row = 2, column = 0, columnspan= 2, padx=40, pady= 10)
        
        self.refresh_serial_devices_button.grid(row = 3, column = 0,)
        self.connet_button.grid(row = 3, column = 1)
        self.server_launch_button.grid(row=4,column=0, columnspan=2)
        #self.server_stop_button.grid(row=4,column=1)
        
        # Others Settings
        self.baudrate_combobox.current(0) # No esta seleccionado
    
    # Regresemos como variables globales lo seleccionado
    def return_bauds(self) :
        return self.baudrate_combobox.get()

    def return_device(self) :
        return self.serial_devices_combobox.get()
    
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
                return
            
            self.serial_device = SerialSensor(
                port = port,
                baudrate = baudrate
            ) 
            
            if self.serial_device.is_open():
                messagebox.showinfo('Connection Successful', f'Control connected successfully on {port} with baudrate {baudrate}')
                
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
    
    # - Server Init - #
    def _create_server_but(self) -> Button:
        return Button(
            master = self,
            text = 'Server Init',
            command = self.server_init,
            width=20,
            cursor='spider',
            font=("Helvetica",12,"bold")
        )
    
    # - Server Stop - #
    def _create_server_stop_but(self) -> Button:
        return Button(
            master=self,
            text='Stop Server',
            command=self.server_stop,
            width=20,
            cursor='spider',
            font=("Helvetica", 12, "bold")
        )
    
    # - Operativo. Corremos el server - #
    def server_init(self):
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    def run_server(self):
        subprocess.run(["python3", "./Server/server.py"])
        self.server_process.communicate()  # Espera a que el proceso termine
    
    # - Operativo. Cerramos el server - #
    def server_stop(self):
        if self.server_process and self.server_process.poll() is None:  # Comprueba si el proceso sigue en ejecución
            os.kill(self.server_process.pid, signal.SIGTERM)  # Envía la señal SIGTERM
            self.server_process.wait()  # Espera a que el proceso termine
            messagebox.showinfo('Server Stopped', 'The server has been stopped successfully.')
        else:
            messagebox.showinfo('Server Not Running', 'The server is not running.')
        
# Credits Frame   
class FrameFour(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        # - Inicializamos los elemntos  - #
        self.creators_names_label: Label = self._create_creators_names_label()
        self.title_label: Label = self._create_Credits_label()
        self.main_txt: Text = self._create_credits_text()
        
        # - Agregamos los credits - #
        # Juegos
        self.main_txt.insert('1.0','Games provided by:\n')
        self.main_txt.insert('2.0',' - 1945 by Haroon Khalid\n')
        self.main_txt.insert('3.0',' - Aseivo by Axel Camacho Villafuerte\n')
        self.main_txt.insert('4.0',' - PyDoom by StanislavPetrovV\n')
        
        # Nostros 
        self.main_txt.insert('5.0',' \n')
        self.main_txt.insert('6.0','Crafted with passion and love by NestSystems Inc. Team:\n')
        self.main_txt.insert('7.0',' - Guadalupe Paulina López Cuevas - A01701095\n')
        self.main_txt.insert('8.0',' - Jorge Israel Sandoval Sánchez - A017010373\n')
        self.main_txt.insert('9.0',' - Jose Alberto Aguilar Sanchez - A01735612\n')
        
        # Agradecimientos
        self.main_txt.insert('11.0',' \n')
        self.main_txt.insert('12.0','And lastley special thanks for: \n')
        self.main_txt.insert('13.0',' - Mum and Dad for always staying with me <3 \n')
        self.main_txt.insert('14.0',' - Aseivo for the help coding\n')
        self.main_txt.insert('15.0',' - Rick for being my reason to continue studying\n')
        self.main_txt.insert('16.0',' - Carracedo for the trust on me\n')
        
        self.main_txt.config(state='disabled')

        self.init_gui()
        
    # Inicialziamos los elemntos graficos
    def init_gui(self,) -> None:
        self.title_label.grid(row=0, column=0, columnspan=2,padx=40)
        self.main_txt.grid(row=1, column=0,columnspan=2,rowspan=3, padx=5)
        self.creators_names_label.grid(row=4, column=0, sticky="w")
    
    # -- Funciones -- #    
    # - Titulo - #
    def _create_Credits_label(self) -> Label:
        return Label(
            master = self,
            text = 'Credits',
            foreground = 'black',
            font=("Z003",20,"bold")
        )
    
    # - Contenido - #
    def _create_credits_text(self) -> Text:
        return Text(
            master=self,
            width=60,
            height= 10
        )
    
    # US
    def _create_creators_names_label(self) -> Label:
        local_label = Label(
            master = self,
            text = 'With love: Paulina, Israel and Azuki',
            foreground = 'black',
            font=("Courier", 10),
            cursor='heart'
        )
        local_label.bind("<Button-1>", self.on_label_click)  # Bind left mouse click event
        return local_label
    
    # And an special message...
    def on_label_click(self, event):
        messagebox.showinfo(
            title="The wind rises!!!", 
            message="Hope this proyect helps and inspire people around the world to continue imagineering")
        
        print("Escúchame, niño japonés. \nLos aviones no son útiles para la guerra.")
        print("No son para hacer dinero. \nLos aviones son hermosos sueños.\n")
        print("Los ingenieros convierten los sueños en realidad.")
        print("- Con amor Caproni")
        
# ------------------------------------------------------ #

root = Tk()

if __name__ == '__main__':
    # Inicializar el servidor primero
    server = GameServer(host='0.0.0.0', port=3333)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    
    # Inicio de app
    ex = App(root)
    root.mainloop()
    
    