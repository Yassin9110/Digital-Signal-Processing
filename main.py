import tkinter as tk
from tkinter import ttk
from subprocess import Popen


# Create the main window
root = tk.Tk()
root.title("Welcome to DSP tasks")

def open_task1_file():
    Popen(['python', 'Task1.py'])
def open_task2_file():
    Popen(['python', 'Task2.py'])
def open_task3_file():
    Popen(['python', 'Task3.py'])
def open_task4_file():
    Popen(['python', 'Task4.py'])
def open_task5_file():
    Popen(['python', 'Task5.py'])
def open_task6_file():
    Popen(['python', 'Task6.py'])
def open_task7_file():
    Popen(['python', 'Task7.py'])
def open_task8_file():
    Popen(['python', 'Task8.py'])

header_label = tk.Label(root, text= "(⁠✷⁠‿⁠✷⁠) (⁠✷⁠‿⁠✷⁠) Welcome Dr.Omar (⁠✷⁠‿⁠✷⁠) (⁠✷⁠‿⁠✷⁠)")
task1_button = ttk.Button(root, text="Task1", command=open_task1_file)
task2_button = ttk.Button(root, text="Task2", command=open_task2_file)
task3_button = ttk.Button(root, text="Task3", command=open_task3_file)
task4_button = ttk.Button(root, text="Task4", command=open_task4_file)
task5_button = ttk.Button(root, text="Task5", command=open_task5_file)
task6_button = ttk.Button(root, text="Task6", command=open_task6_file)
task7_button = ttk.Button(root, text="Task7", command=open_task7_file)
task8_button = ttk.Button(root, text="Task8", command=open_task8_file)
footer_label = tk.Label(root, text="Credits to Yassin & Youssef")


root.geometry("400x400")

header_label.pack(side='top')
task1_button.pack(pady=10)
task2_button.pack(pady=10)
task3_button.pack(pady=10)
task4_button.pack(pady=10)
task5_button.pack(pady=10)
task6_button.pack(pady=10)
task7_button.pack(pady=10)
task8_button.pack(pady=10)
footer_label.pack(side="bottom")


root.mainloop()