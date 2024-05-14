import math

import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from Task4_Test import  RoundPhaseShift, SignalComapreAmplitude,SignalComaprePhaseShift
def calculate_dft(signal):
    N = len(signal)
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        X[k] = 0
        for n in range(N):
            X[k] += signal[n] * np.exp(-2j * np.pi * k * n / N)

    return X

x_test = []
y_test = []


def ReadTest():
    global x_test
    x_test = []
    global y_test
    y_test = []
    file_path = filedialog.askopenfilename()
    if (file_path):
        with open(file_path, 'r') as file:
            file.readline()
            file.readline()
            N = int(file.readline())
            lines = file.readlines()
            for line in lines:
                data = line.split()
                x_test.append(round(float(data[0].rstrip("f")), 6))
                y_test.append(round(float(data[1].rstrip("f")), 6))
            file.close()
def calculate_magnitude(X_k):
    magnitude = np.sqrt(X_k.real ** 2 + X_k.imag ** 2)
    return magnitude

def calculate_phase(X_k):
    phases = np.arctan2(np.imag(X_k), np.real(X_k))
    return phases

def plot_frequency_domain(signal, sampling_frequency):
    N = len(signal)
    frequencies = np.arange(N) * sampling_frequency / N
    X = calculate_dft(signal)

    amplitudes = [calculate_magnitude(X_k) for X_k in X]
    phases = [calculate_phase(X_k) for X_k in X]

    for k, X_k in enumerate(X):
        magnitude = calculate_magnitude(X_k)
        phase = calculate_phase(X_k)

        print(f'X({k}) = {X_k}')
        print(f'Magnitude (A) = {magnitude}')
        print(f'Phase (Phi) = {phase} degrees')

    # Plot frequency versus amplitude and phase
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.stem(frequencies, amplitudes)
    plt.title('Frequency vs. Amplitude')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')

    plt.subplot(2, 1, 2)
    plt.stem(frequencies, phases)
    plt.title('Frequency vs. Phase (Degrees)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase (Degrees)')

    plt.tight_layout()
    plt.show()

# Time Domain Signal Functions
def calculate_idft(X):
    N = len(X)
    signal = np.zeros(N, dtype=complex)

    for n in range(N):
        signal[n] = 0
        for k in range(N):
            angle = 2 * np.pi * n * k / N
            real_part = np.cos(angle)
            imaginary_part = np.sin(angle)
            signal[n] += (X[k].real * real_part) - (X[k].imag * imaginary_part)

        signal[n] /= N

    return signal.real

def display_results(results):
    if results:
        x_n = "{" + ", ".join([f"{result:.4f}" for result in results]) + "}"
        print(f'x(n) = {x_n}')

def display_plots():
    image = Image.open("time_domain_plot.png")
    image.show()

# GUI Functions
def browse_file():

    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def save_file(X, omit_phase=False):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            for k, X_k in enumerate(X):
                magnitude = calculate_magnitude(X_k)
                if omit_phase:
                    file.write(f'X({k}) = {magnitude:.4f}\n')
                else:
                    phase = calculate_phase(X_k)
                    file.write(f'X({k}) = {magnitude:.4f},{phase:.4f} degrees\n')

def save_file2(X, omit_phase=False):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            for k, X_k in enumerate(X):
                magnitude = calculate_magnitude(X_k)
                if omit_phase:
                    file.write(f'X({k}) = {magnitude:.4f}\n')
                else:
                    phase = calculate_phase(X_k)
                    file.write(f'X({k}) = {magnitude:.4f}')

def process_dft():
    file_path = file_entry.get()
    try:
        sampling_frequency = float(sampling_entry.get())
        amplitude_str = amplitude_entry.get()
        phase_str = phase_entry.get()

        with open(file_path, 'r') as file:
            lines = file.readlines()
            signal = [float(line.strip().split()[1]) for line in lines[3:] if len(line.strip().split()) == 2]

        if amplitude_str and phase_str:
            amplitude = float(amplitude_str)
            phase_degrees = float(phase_str)
            phase_radians = np.radians(phase_degrees)  # Convert degrees to radians

            signal_component = amplitude * np.exp(1j * phase_radians)
            frequency_component_index = 0
            signal[frequency_component_index] = signal_component.real

        X = calculate_dft(signal)
        frequencies = [math.sqrt((pow(val.real, 2) + pow(val.imag, 2))) for val in X]
        print (frequencies)
        ReadTest()
        print(x_test)
        print(SignalComapreAmplitude([round(row, 6) for row in frequencies],x_test))
        save_file(X)  # Save DFT results

        plot_frequency_domain(signal, sampling_frequency)
    except Exception as e:
        print(f"Error: {e}")

def process_idft():
    file_path = file_entry.get()
    try:
        X = []

        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines[3:]:
                values = line.strip().replace(",", " ").split()
                if len(values) == 2:
                    amplitude_str = values[0].replace("f", "")
                    phase_str = values[1].replace("f", "")
                    amplitude = float(amplitude_str)
                    phase = float(phase_str)
                    complex_value = amplitude * (np.cos(phase) + 1j * np.sin(phase))
                    X.append(complex_value)

        amplitude_str = amplitude_entry.get()
        phase_str = phase_entry.get()

        if amplitude_str and phase_str:
            amplitude = float(amplitude_str)
            phase_degrees = float(phase_str)
            phase_radians = np.radians(phase_degrees)
            modified_component = amplitude * np.exp(1j * phase_radians)
            frequency_component_index = 0
            X[frequency_component_index] = modified_component

        signal = calculate_idft(X)
        results = signal.tolist()
        display_results(results)
        ReadTest()
        real_values = [round(x.real, 6) for x in results]
        plot_time_domain(real_values)
        print(SignalComapreAmplitude(real_values, y_test))
        print(x_test)
        print(real_values)
        save_file2(results)  # Save modified IDFT results
    except Exception as e:
        print(f"Error: {e}")

def plot_time_domain(signal):
    N = len(signal)
    time = np.arange(N)

    # Plot time domain signal
    plt.figure(figsize=(12, 6))
    plt.plot(time, signal)
    plt.title('Time Domain Signal')
    plt.xlabel('Time (samples)')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.savefig("time_domain_plot.png")
    plt.show()
    plt.close()

window = tk.Tk()
window.title("Signal Analysis")
window.geometry("400x600")  # Adjusted window height for additional input fields

file_label = tk.Label(window, text="Select a file:")
file_label.pack(pady=10)

file_entry = tk.Entry(window, width=30)
file_entry.pack()

browse_button = tk.Button(window, text="Browse", command=browse_file)
browse_button.pack()

sampling_label = tk.Label(window, text="Enter Sampling Frequency (Hz):")
sampling_label.pack(pady=10)

sampling_entry = tk.Entry(window, width=10)
sampling_entry.pack()

amplitude_label = tk.Label(window, text="Amplitude:")
amplitude_label.pack(pady=10)
amplitude_entry = tk.Entry(window, width=10)
amplitude_entry.pack()

phase_label = tk.Label(window, text="Phase (degrees):")
phase_label.pack(pady=10)
phase_entry = tk.Entry(window, width=10)
phase_entry.pack()

dft_button = tk.Button(window, text="Process DFT", command=process_dft)
dft_button.pack(pady=10)

idft_button = tk.Button(window, text="Process IDFT", command=process_idft)
idft_button.pack(pady=10)

# Start the GUI main loop
window.mainloop()