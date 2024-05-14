# import numpy as np
# import matplotlib.pyplot as plt
# import tkinter as tk
# from tkinter import filedialog
#
# def calculate_dft(signal):
#     N = len(signal)
#     X = np.fft.fft(signal)
#     frequencies = np.fft.fftfreq(N)
#     return X, frequencies
#
# def calculate_magnitude(X_k):
#     magnitude = np.abs(X_k)
#     return magnitude
#
# def calculate_phase(X_k):
#     phase = np.angle(X_k)
#     return phase
#
# def remove_dc_component(signal, frequencies):
#     X, _ = calculate_dft(signal)
#
#     # Identify the index corresponding to DC
#     dc_index = np.argmax(frequencies >= 0)
#
#     # Set the DC component to zero
#     X[dc_index] = 0
#
#     # Calculate inverse DFT to get the filtered signal
#     dc_removed_signal = np.fft.ifft(X)
#     return dc_removed_signal.real
#
# def plot_frequency_domain(signal, sampling_frequency, frequencies):
#     X, _ = calculate_dft(signal)
#     amplitudes = [calculate_magnitude(X_k) for X_k in X]
#     phases = [calculate_phase(X_k) for X_k in X]
#
#     plt.figure(figsize=(12, 6))
#     plt.subplot(2, 1, 1)
#     plt.stem(frequencies, amplitudes)
#     plt.title('Frequency vs. Amplitude')
#     plt.xlabel('Frequency (Hz)')
#     plt.ylabel('Amplitude')
#
#     plt.subplot(2, 1, 2)
#     plt.stem(frequencies, phases)
#     plt.title('Frequency vs. Phase (Radians)')
#     plt.xlabel('Frequency (Hz)')
#     plt.ylabel('Phase (Radians)')
#
#     plt.tight_layout()
#     plt.show()
#
# def browse_file():
#     file_path = filedialog.askopenfilename()
#     if file_path:
#         file_entry.delete(0, tk.END)
#         file_entry.insert(0, file_path)
#
# def process_dft():
#     file_path = file_entry.get()
#     try:
#         sampling_frequency = float(sampling_entry.get())
#
#         with open(file_path, 'r') as file:
#             lines = file.readlines()
#             signal = [float(line.strip().split()[1]) for line in lines[3:] if len(line.strip().split()) == 2]
#
#         frequencies = np.fft.fftfreq(len(signal), d=1/sampling_frequency)
#
#         if remove_dc_var.get():
#             dc_removed_signal = remove_dc_component(signal, frequencies)
#             print("Signal after removing DC component:")
#             for i, value in enumerate(dc_removed_signal):
#                 print(f"{i} {value:.4f}")
#             plot_frequency_domain(dc_removed_signal, sampling_frequency, frequencies)
#         else:
#             plot_frequency_domain(signal, sampling_frequency, frequencies)
#     except Exception as e:
#         print(f"Error: {e}")
#
# window = tk.Tk()
# window.title("Signal Analysis")
# window.geometry("400x650")
#
# file_label = tk.Label(window, text="Select a file:")
# file_label.pack(pady=10)
#
# file_entry = tk.Entry(window, width=30)
# file_entry.pack()
#
# browse_button = tk.Button(window, text="Browse", command=browse_file)
# browse_button.pack()
#
# sampling_label = tk.Label(window, text="Enter Sampling Frequency (Hz):")
# sampling_label.pack(pady=10)
#
# sampling_entry = tk.Entry(window, width=10)
# sampling_entry.pack()
#
# remove_dc_var = tk.IntVar()
# remove_dc_button = tk.Checkbutton(window, text="Remove DC component", variable=remove_dc_var)
# remove_dc_button.pack(pady=10)
#
# dft_button = tk.Button(window, text="Process DFT", command=process_dft)
# dft_button.pack(pady=10)
#
# window.mainloop()

import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

def calculate_dft(signal):
    N = len(signal)
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        X[k] = 0
        for n in range(N):
            X[k] += signal[n] * np.exp(-2j * np.pi * k * n / N)
    return X

def calculate_magnitude(X_k):
    magnitude = np.abs(X_k)
    return magnitude

def calculate_phase(X_k):
    phase = np.angle(X_k)
    return phase

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

    return np.asarray(signal, float)

def remove_dc_component(signal, frequencies):
    X = calculate_dft(signal)

    # Identify the index corresponding to DC
    dc_index = np.argmax(frequencies >= 0)

    # Set the DC component to zero
    X[dc_index] = 0

    # Calculate inverse DFT to get the filtered signal
    dc_removed_signal = calculate_idft(X)
    return dc_removed_signal.real

def plot_frequency_domain(signal, sampling_frequency, frequencies):
    X = calculate_dft(signal)
    amplitudes = [calculate_magnitude(X_k) for X_k in X]
    phases = [calculate_phase(X_k) for X_k in X]

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.stem(frequencies, amplitudes)
    plt.title('Frequency vs. Amplitude')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')

    plt.subplot(2, 1, 2)
    plt.stem(frequencies, phases)
    plt.title('Frequency vs. Phase (Radians)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase (Radians)')

    plt.tight_layout()
    plt.show()

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def process_dft():
    file_path = file_entry.get()
    try:
        sampling_frequency = float(sampling_entry.get())

        with open(file_path, 'r') as file:
            lines = file.readlines()
            signal = [float(line.strip().split()[1]) for line in lines[3:] if len(line.strip().split()) == 2]

        frequencies = np.fft.fftfreq(len(signal), d=1/sampling_frequency)

        if remove_dc_var.get():
            dc_removed_signal = remove_dc_component(signal, frequencies)
            print("Signal after removing DC component:")
            for i, value in enumerate(dc_removed_signal):
                print(f"{i} {value:.4f}")
            plot_frequency_domain(dc_removed_signal, sampling_frequency, frequencies)
        else:
            plot_frequency_domain(signal, sampling_frequency, frequencies)
    except Exception as e:
        print(f"Error: {e}")

window = tk.Tk()
window.title("Signal Analysis")
window.geometry("400x650")

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

remove_dc_var = tk.IntVar()
remove_dc_button = tk.Checkbutton(window, text="Remove DC component", variable=remove_dc_var)
remove_dc_button.pack(pady=10)

dft_button = tk.Button(window, text="Process DFT", command=process_dft)
dft_button.pack(pady=10)

window.mainloop()
