import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
import matplotlib.pyplot as plt
from Task6_Shift_Fold_Signal_Test import Shift_Fold_Signal

def read_signal_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    signal_type = int(lines[0].strip())
    is_periodic = int(lines[1].strip())
    n_samples = int(lines[2].strip())

    data_lines = lines[3:]

    signal_data = []

    for line in data_lines:
        values = list(map(float, line.strip().split()))
        signal_data.append(values)

    return signal_type, is_periodic, n_samples, np.array(signal_data)

def fold_signal(signal):
    return np.flip(signal[:, 1])

def plot_signals(time, original_signal, processed_signal, operation):
    plt.plot(time, original_signal, label='Original Signal')
    plt.plot(time, processed_signal, label=f'Signal after {operation}')

def browse_file(file_directory_var):
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        file_directory_var.set(filename)

def start_processing(file_directory_var):
    filename = file_directory_var.get()
    if not filename:
        messagebox.showinfo("Select File", "Please select a signal file.")
        return

    signal_type, is_periodic, n_samples, signal_data = read_signal_file(filename)
    time = signal_data[:, 0] if signal_type == 0 else np.arange(n_samples)

    processed_signal = fold_signal(signal_data)

    plot_signals(time, signal_data[:, 1], processed_signal, 'Fold')
    plt.title('Signal after Fold')
    plt.xlabel('Sample Index')
    plt.legend()
    plt.show()

    Shift_Fold_Signal("Task6\TestCases\Shifting and Folding\Output_fold.txt", time, processed_signal)

# GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Signal Processor - Fold Operation")
    root.geometry("350x125")

    # File directory
    file_directory_var = tk.StringVar()

    file_frame = ttk.Frame(root)
    file_frame.pack()

    file_label = tk.Label(file_frame, text="Choose Signal File:")
    file_label.grid(row=0, column=0)

    file_directory_entry = tk.Entry(file_frame, textvariable=file_directory_var, state='disabled')
    file_directory_entry.grid(row=0, column=1)

    file_button = ttk.Button(file_frame, text="Browse", command=lambda: browse_file(file_directory_var))
    file_button.grid(row=0, column=2)

    # Process button
    process_button = ttk.Button(root, text="Process Signal", command=lambda: start_processing(file_directory_var))
    process_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
