import tkinter as tk
from tkinter import ttk
from subprocess import Popen


# Create the main window
root = tk.Tk()
root.title("Task 6")

def open_smoothing_file():
    Popen(['python', 'Task6_smooth.py'])
def open_sharping_file():
    Popen(['python', 'Task6_Sharping.py'])
def open_delayoradvance_file():
    Popen(['python', 'Task6_delayoradvans.py'])
def open_folding_file():
    Popen(['python', 'Task6_folding.py'])
def open_shiftFolded_file():
    Popen(['python', 'Task6_ShiftFold.py'])
def open_RemoveDC_file():
    Popen(['python', 'Task6_DC compo.py'])
def open_convolution_file():
    Popen(['python', 'Task6_conv.py'])


task1_button = ttk.Button(root, text="Smoothing", command=open_smoothing_file)
task2_button = ttk.Button(root, text="Sharping", command=open_sharping_file)
task3_button = ttk.Button(root, text="Shifting", command=open_delayoradvance_file)
task4_button = ttk.Button(root, text="Folding", command=open_folding_file)
task5_button = ttk.Button(root, text="Shift folded", command=open_shiftFolded_file)
task6_button = ttk.Button(root, text="Remove DC", command=open_RemoveDC_file)
task7_button = ttk.Button(root, text="Convolution", command=open_convolution_file)

footer_label = tk.Label(root, text="Credits to Yassin & Youssef")


root.geometry("400x350")

task1_button.pack(pady=10)
task2_button.pack(pady=10)
task3_button.pack(pady=10)
task4_button.pack(pady=10)
task5_button.pack(pady=10)
task6_button.pack(pady=10)
task7_button.pack(pady=10)

footer_label.pack(side="bottom")


root.mainloop()