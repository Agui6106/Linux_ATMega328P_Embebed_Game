"""
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

"""

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


