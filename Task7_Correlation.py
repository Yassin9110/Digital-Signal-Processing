import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from Task7_corr_test import Compare_Signals


def read_signal_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    signal_type = int(lines[0].strip())
    is_periodic = int(lines[1].strip())
    n_samples = int(lines[2].strip())

    data_lines = lines[3:]

    signal_data = []

    for line in data_lines:
        values = list(map(float, line.strip().split()))
        signal_data.append(values)

    return np.array(signal_data)


def cross_correlation(x1, x2):
    N = len(x1)
    cross_corr_result = []

    for n in range(N):
        cross_corr_value = 1 / N * sum(x1[j] * x2[(j + n) % N] for j in range(N))
        cross_corr_result.append(cross_corr_value)


    print("Cross result is: ", cross_corr_result)

    return cross_corr_result


def normalized_cross_correlation(x1, x2):
    N = len(x1)

    if N == 0:
        raise ValueError("Length of signals must be greater than zero.")

    # Calculate the cross-correlation function r12(n)
    cross_corr_result = cross_correlation(x1, x2)

    # Calculate the normalization factor
    norm_factor = (1 / N) * sum(x1[j] ** 2 for j in range(N)) * (1 / N) * sum(x2[j] ** 2 for j in range(N))

    # Check for division by zero
    if norm_factor == 0:
        raise ValueError("Normalization factor is zero. Unable to divide by zero.")

    norm_factor = np.sqrt(norm_factor)

    # Normalize the cross-correlation function
    normalized_corr_result = [r12_n / norm_factor for r12_n in cross_corr_result]

    return normalized_corr_result


def process_files(file_path1, file_path2):
    # Read signals from files
    signal_data1 = read_signal_file(file_path1)
    signal_data2 = read_signal_file(file_path2)

    # Extract samples
    samples_signal1 = signal_data1[:, 1]
    samples_signal2 = signal_data2[:, 1]

    # Compute normalized cross-correlation
    normalized_corr_result = normalized_cross_correlation(samples_signal1, samples_signal2)
    indices = []

    # Display the result and plot the signals
    print("Normalized Cross-Correlation Result:")
    for i, value in enumerate(normalized_corr_result):
        indices.append(i)
        print(f"{i} {value}")

    Compare_Signals("Task7\Task Files\Point1 Correlation\CorrOutput.txt", indices, normalized_corr_result)

    # Plot the signals
    plt.figure(figsize=(10, 6))

    plt.subplot(3, 1, 1)
    plt.plot(signal_data1[:, 0], samples_signal1, label='Signal 1')
    plt.title('Signal 1')
    plt.xlabel('Index')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(signal_data2[:, 0], samples_signal2, label='Signal 2')
    plt.title('Signal 2')
    plt.xlabel('Index')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(indices, normalized_corr_result, label='Normalized Cross-Correlation')
    plt.title('Normalized Cross-Correlation Result')
    plt.xlabel('Index')
    plt.ylabel('Correlation Value')
    plt.legend()

    plt.tight_layout()
    plt.show()


# GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Normalized Cross-Correlation Processor")
    root.geometry("400x300")

    file_path_var1 = tk.StringVar()
    file_path_var2 = tk.StringVar()

    file_frame = tk.Frame(root)
    file_frame.pack()

    file_label1 = tk.Label(file_frame, text="Choose Signal File 1:")
    file_label1.grid(row=0, column=0)

    file_entry1 = tk.Entry(file_frame, textvariable=file_path_var1, state='disabled')
    file_entry1.grid(row=0, column=1)

    file_button1 = tk.Button(file_frame, text="Browse", command=lambda: browse_file(file_path_var1))
    file_button1.grid(row=0, column=2)

    file_label2 = tk.Label(file_frame, text="Choose Signal File 2:")
    file_label2.grid(row=1, column=0)

    file_entry2 = tk.Entry(file_frame, textvariable=file_path_var2, state='disabled')
    file_entry2.grid(row=1, column=1)

    file_button2 = tk.Button(file_frame, text="Browse", command=lambda: browse_file(file_path_var2))
    file_button2.grid(row=1, column=2)

    process_button = tk.Button(root, text="Process Signals",
                               command=lambda: process_files(file_path_var1.get(), file_path_var2.get()))
    process_button.pack(pady=10)

    root.mainloop()


def browse_file(file_path_var):
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        file_path_var.set(filename)


# Run the GUI
create_gui()
