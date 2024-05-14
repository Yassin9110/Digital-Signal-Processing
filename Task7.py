import tkinter as tk
from tkinter import ttk
from subprocess import Popen


# Create the main window
root = tk.Tk()
root.title("Task 7")

def open_Correlation_file():
    Popen(['python', 'Task7_Correlation.py'])
def open_Time_Analysis_file():
    Popen(['python', 'Task7_Time_Analysis.py'])
def open_Template_matching_file():
    Popen(['python', 'Task7_Template_matching.py'])



task1_button = ttk.Button(root, text="Correlation", command=open_Correlation_file)
task2_button = ttk.Button(root, text="Time_Analysis", command=open_Time_Analysis_file)
task3_button = ttk.Button(root, text="Template_matching", command=open_Template_matching_file)


footer_label = tk.Label(root, text="Credits to Yassin & Youssef")


root.geometry("400x160")

task1_button.pack(pady=10)
task2_button.pack(pady=10)
task3_button.pack(pady=10)


footer_label.pack(side="bottom")


root.mainloop()