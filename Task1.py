import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from tkinterdnd2 import DND_FILES, TkinterDnD
from subprocess import Popen


# Define a function to display continuous and discrete signals
def plot_signal_continuous(t, signal, title):
    plt.figure()
    plt.title(title)
    plt.plot(t, signal)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

def plot_signal_discrete(t, signal, title):
    plt.title(title)
    plt.stem(t, signal)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

# Define a function to generate sine or cosine waves
def generate_signal(A, analog_frequency, sampling_frequency, phase_shift, wave_type, time_duration, is_continuous):
    if is_continuous:
        t = np.arange(0, time_duration, 0.001)
    else:
        t = np.arange(0, time_duration, 1 / sampling_frequency)

    if wave_type == 'sine':
        signal = A * np.sin(2 * np.pi * analog_frequency * t + phase_shift)
    else:
        signal = A * np.cos(2 * np.pi * analog_frequency * t + phase_shift)

    return t, signal

# Define a function to handle the signal generation button
def generate_signal_handler():
    A = float(amp_entry.get())
    analog_frequency = float(analog_freq_entry.get())
    sampling_frequency = float(sampling_freq_entry.get())
    phase_shift = float(phase_shift_entry.get())
    wave_type = wave_type_var.get()
    time_duration = float(time_duration_entry.get())  # Get the time duration from the entry field
    is_continuous = continuous_var.get()

    if sampling_frequency < 2 * analog_frequency:
        error_message = "Sampling frequency must be at least 2 times the analog frequency."
        messagebox.showerror("Error", error_message)
    else:
        t, signal = generate_signal(A, analog_frequency, sampling_frequency, phase_shift, wave_type, time_duration, is_continuous)

        if is_continuous:
            plot_signal_continuous(t, signal, 'Generated Signal')
        else:
            plot_signal_discrete(t, signal, 'Generated Signal')
        plt.show()

# Define a function to handle the load signal button
def load_signal_handler():
    file_path = file_path_entry.get()
    load_signal(file_path)

def load_signal(file_path):
    t, signal = read_samples_from_file(file_path)
    if t is not None:
        # Plot the loaded signal
        plot_signal_continuous(t, signal, 'Loaded Signal - Continuous')
        plot_signal_discrete(t, signal, 'Loaded Signal - Discrete')
        plt.show()

# Define a function to read samples from a text file
def read_samples_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        t = []
        data = []

        for line in lines:
            parts = line.split()
            if len(parts) == 2:
                t.append(float(parts[0]))
                data.append(float(parts[1]))

        return np.array(t), np.array(data)
    except Exception as e:
        print(f"Error reading file: {e}")
        return np.array([]), np.array([])

# Create the main GUI window
root = TkinterDnD.Tk()
root.title("Signal Processing Framework")

# Create a notebook for multiple tabs
notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10)

# Tab for Signal Generation
signal_gen_frame = ttk.Frame(notebook)
notebook.add(signal_gen_frame, text='Signal Generation')

# Signal generation widgets
ttk.Label(signal_gen_frame, text="Amplitude (A):").grid(row=0, column=0)
amp_entry = ttk.Entry(signal_gen_frame)
amp_entry.grid(row=0, column=1)

ttk.Label(signal_gen_frame, text="Analog Frequency (Hz):").grid(row=1, column=0)
analog_freq_entry = ttk.Entry(signal_gen_frame)
analog_freq_entry.grid(row=1, column=1)

ttk.Label(signal_gen_frame, text="Sampling Frequency (Hz):").grid(row=2, column=0)
sampling_freq_entry = ttk.Entry(signal_gen_frame)
sampling_freq_entry.grid(row=2, column=1)

ttk.Label(signal_gen_frame, text="Phase Shift (radians):").grid(row=3, column=0)
phase_shift_entry = ttk.Entry(signal_gen_frame)
phase_shift_entry.grid(row=3, column=1)

ttk.Label(signal_gen_frame, text="Time Duration (s):").grid(row=4, column=0)
time_duration_entry = ttk.Entry(signal_gen_frame)
time_duration_entry.grid(row=4, column=1)

wave_type_var = tk.StringVar()
ttk.Radiobutton(signal_gen_frame, text="Sine Wave", variable=wave_type_var, value="sine").grid(row=5, column=0)
ttk.Radiobutton(signal_gen_frame, text="Cosine Wave", variable=wave_type_var, value="cosine").grid(row=5, column=1)

generate_button = ttk.Button(signal_gen_frame, text="Generate Signal", command=generate_signal_handler)
generate_button.grid(row=6, column=0, columnspan=2)

continuous_var = tk.IntVar(value=1)
ttk.Checkbutton(signal_gen_frame, text="Continuous Signal", variable=continuous_var).grid(row=7, column=0, columnspan=2)

# Tab for Signal Load
signal_load_frame = ttk.Frame(notebook)
notebook.add(signal_load_frame, text='Load Signal')

# Load signal widgets
ttk.Label(signal_load_frame, text="Load Signal from File:").grid(row=0, column=0, columnspan=2)
ttk.Label(signal_load_frame, text="File Path:").grid(row=1, column=0)
file_path_entry = ttk.Entry(signal_load_frame)
file_path_entry.grid(row=1, column=1)

load_button = ttk.Button(signal_load_frame, text="Load Signal", command=load_signal_handler)
load_button.grid(row=2, column=0, columnspan=2)

ttk.Label(signal_load_frame, text="Drag and Drop File Here:").grid(row=3, column=0, columnspan=2)
signal_load_frame.drop_target_register(DND_FILES)
signal_load_frame.dnd_bind('<<Drop>>', lambda event: load_signal(event.data))
# Create a function to open the second file when the button is clicked
# Create a new frame for the second file button
second_file_frame = ttk.Frame(signal_gen_frame)
second_file_frame.grid(row=8, column=0, columnspan=2)

def open_second_file():
    Popen(['python', "D:\Fcis\Year3\DSP/Task2.py"])

open_second_file_button = ttk.Button(second_file_frame, text="Operations", command=open_second_file)
open_second_file_button.pack()
# Start the main loop
root.mainloop()