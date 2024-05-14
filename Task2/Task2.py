import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import os

def open_file(file_list):
    file_path = filedialog.askopenfilename(filetypes=[("Signal files", "*.txt")])
    if file_path:
        file_list.append(file_path)
        file_listbox.insert(tk.END, file_path)

def remove_file(file_list, selected_index):
    if selected_index >= 0 and selected_index < len(file_list):
        file_path = file_list.pop(selected_index)
        file_listbox.delete(selected_index)
        print("Removed:", file_path)

def clear_files(file_list):
    file_listbox.delete(0, tk.END)
    file_list.clear()
    print("Cleared all files")

def shift_signal(file, shift_value):
    data = np.genfromtxt(file, skip_header=3)
    time, amplitude = data[:, 0], data[:, 1]
    shifted_time, shifted_amplitude = time + shift_value, amplitude
    filename = os.path.basename(file)  # Extracting the filename from the path
    fig, ax = plt.subplots()
    ax.plot(time, amplitude, label=f"{filename} (Original)")
    ax.plot(shifted_time, shifted_amplitude, label=f"{filename} (Shifted)")
    ax.set_xlabel('Time (t)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Resulting Signal (Shifted)')
    ax.legend()
    plt.show()

def read_signal(file_path):
    try:
        with open(file_path, 'r') as file:
            signal_type = int(file.readline().strip())
            is_periodic = int(file.readline().strip())
            n_samples = int(file.readline().strip())

            signal_data = []
            for _ in range(n_samples):
                if signal_type == 0:
                    sample_index, sample_amplitude = map(int, file.readline().strip().split())
                    signal_data.append((sample_index, sample_amplitude))
                elif signal_type == 1:
                    frequency, amplitude, phase_shift = map(float, file.readline().strip().split())
                    signal_data.append((frequency, amplitude, phase_shift))

            return signal_type, is_periodic, signal_data
    except:
        print("Error reading the signal file:", file_path)
        return None

def perform_addition(file_list):
    if len(file_list) < 2:
        print("Select at least two input files for the addition operation.")
        return

    result_signal = None
    max_samples = 0

    # Find the maximum number of samples among all input signals
    for file_path in file_list:
        signal = read_signal(file_path)
        if signal:
            _, _, signal_data = signal
            max_samples = max(max_samples, len(signal_data))

    # Synchronize the signals by filling missing samples with zeros
    for file_path in file_list:
        signal = read_signal(file_path)
        if signal:
            _, _, signal_data = signal
            # Extend the signal to match the length of the longest signal
            while len(signal_data) < max_samples:
                signal_data.append((len(signal_data), 0))
            if result_signal is None:
                result_signal = np.array(signal_data)
            else:
                # Perform element-wise addition using NumPy
                result_signal = np.add(result_signal, np.array(signal_data))

    plot_result_signal(result_signal)

def perform_subtraction(file_list):
    if len(file_list) < 2:
        print("Select at least two input files for the subtraction operation.")
        return

    result_signal = None
    max_samples = 0

    # Find the maximum number of samples among all input signals
    for file_path in file_list:
        signal = read_signal(file_path)
        if signal:
            _, _, signal_data = signal
            max_samples = max(max_samples, len(signal_data))

    # Synchronize the signals by filling missing samples with zeros
    for file_path in file_list:
        signal = read_signal(file_path)
        if signal:
            _, _, signal_data = signal
            # Extend the signal to match the length of the longest signal
            while len(signal_data) < max_samples:
                signal_data.append((len(signal_data), 0))
            if result_signal is None:
                result_signal = np.array(signal_data)
            else:
                # Perform element-wise subtraction using NumPy
                result_signal = np.subtract(result_signal, np.array(signal_data))

    plot_result_signal(result_signal)

def perform_multiplication(file_list, constant):
    if not constant:
        print("Enter a valid constant value for multiplication.")
        return

    if not file_list:
        print("Select at least one input file for multiplication.")
        return

    result_signal = None

    for file_path in file_list:
        signal = read_signal(file_path)
        if signal:
            _, _, signal_data = signal
            # Multiply each data point by the constant value
            multiplied_signal = [(index, amplitude * constant) for index, amplitude in signal_data]
            if result_signal is None:
                result_signal = np.array(multiplied_signal)
            else:
                # Perform element-wise addition using NumPy
                result_signal = np.add(result_signal, np.array(multiplied_signal))

    plot_result_signal(result_signal)

def perform_squaring(file_list):
    if not file_list:
        print("Select at least one input file for squaring.")
        return

    result_signal = None

    for file_path in file_list:
        signal = read_signal(file_path)
        if signal:
            _, _, signal_data = signal
            # Square each data point
            squared_signal = [(index, amplitude ** 2) for index, amplitude in signal_data]
            if result_signal is None:
                result_signal = np.array(squared_signal)
            else:
                # Perform element-wise addition using NumPy
                result_signal = np.add(result_signal, np.array(squared_signal))

    plot_result_signal(result_signal)

def perform_normalization(file_list, normalize_to):
    if not file_list:
        print("Select at least one input file for normalization.")
        return

    if normalize_to == "-1 to 1":
        min_amplitude, max_amplitude = -1, 1
    elif normalize_to == "0 to 1":
        min_amplitude, max_amplitude = 0, 1
    else:
        print("Invalid normalization range. Choose either '-1 to 1' or '0 to 1'.")
        return

    for file_path in file_list:
        signal = read_signal(file_path)
        if signal:
            signal_type, is_periodic, signal_data = signal
            amplitude_values = [sample[1] for sample in signal_data]
            min_value = min(amplitude_values)
            max_value = max(amplitude_values)
            if max_value != min_value:
                normalized_signal = [(index, (amplitude - min_value) / (max_value - min_value) * (max_amplitude - min_amplitude) + min_amplitude) for index, amplitude in signal_data]
                plot_result_signal(np.array(normalized_signal))
            else:
                print("Normalization not applied. All amplitude values are the same.")

def accumulate_signal(file):
    data = np.genfromtxt(file, skip_header=3)
    time, amplitude = data[:, 0], data[:, 1]
    accumulated_amplitude = np.cumsum(amplitude)
    filename = os.path.basename(file)  # Extracting the filename from the path
    fig, ax = plt.subplots()
    ax.plot(time, accumulated_amplitude, label=f"{filename} (Accumulated)")
    ax.set_xlabel('Time (t)')
    ax.set_ylabel('Accumulated Amplitude')
    ax.set_title('Resulting Signal (Accumulation)')
    ax.legend()
    plt.show()

def plot_result_signal(signal):
    plt.plot([sample[1] for sample in signal])  # Extract and plot the amplitudes only
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

# Create the main window
window = tk.Tk()
window.title("Signal Operations")

# Create the file selection widgets
file_list = []
file_label = tk.Label(window, text="Select Signal Files:")
file_label.grid(row=0, column=0, padx=5, pady=5)

file_listbox = tk.Listbox(window, width=50)
file_listbox.grid(row=0, column=1, padx=5, pady=5)

add_file_button = tk.Button(window, text="Add File", command=lambda: open_file(file_list))
add_file_button.grid(row=1, column=0, padx=5, pady=5)

remove_file_button = tk.Button(window, text="Remove File", command=lambda: remove_file(file_list, file_listbox.curselection()[0]))
remove_file_button.grid(row=1, column=1, padx=5, pady=5)

clear_files_button = tk.Button(window, text="Clear Files", command=lambda: clear_files(file_list))
clear_files_button.grid(row=1, column=2, padx=5, pady=5)

# Create the operation buttons
addition_button = tk.Button(window, text="Addition", command=lambda: perform_addition(file_list))
addition_button.grid(row=2, column=0, padx=5, pady=5)

subtraction_button = tk.Button(window, text="Subtraction", command=lambda: perform_subtraction(file_list))
subtraction_button.grid(row=2, column=1, padx=5, pady=5)

# Multiplication constant entry
multiplication_label = tk.Label(window, text="Multiplication Constant:")
multiplication_label.grid(row=3, column=0, padx=5, pady=5)

multiplication_entry = tk.Entry(window)
multiplication_entry.grid(row=3, column=1, padx=5, pady=5)

multiplication_button = tk.Button(window, text="Multiplication", command=lambda: perform_multiplication(file_list, float(multiplication_entry.get())))
multiplication_button.grid(row=3, column=2, padx=5, pady=5)

# Squaring button
squaring_button = tk.Button(window, text="Squaring", command=lambda: perform_squaring(file_list))
squaring_button.grid(row=4, column=0, padx=5, pady=5)

# Normalization options
normalization_label = tk.Label(window, text="Normalization Range:")
normalization_label.grid(row=5, column=0, padx=5, pady=5)

normalize_to_var = tk.StringVar(value="-1 to 1")
normalize_to_option = tk.OptionMenu(window, normalize_to_var, "-1 to 1", "0 to 1")
normalize_to_option.grid(row=5, column=1, padx=5, pady=5)

normalize_button = tk.Button(window, text="Normalize", command=lambda: perform_normalization(file_list, normalize_to_var.get()))
normalize_button.grid(row=5, column=2, padx=5, pady=5)

# Accumulation button
accumulation_button = tk.Button(window, text="Accumulation", command=lambda: perform_accumulation(file_list))
accumulation_button.grid(row=6, column=0, padx=5, pady=5)
def perform_accumulation(file_list):
    if not file_list:
        print("Select at least one input file for accumulation.")
        return

    for file_path in file_list:
        accumulate_signal(file_path)
# Start the GUI
window.mainloop()