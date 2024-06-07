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
   
   """

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