import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate

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

def cross_correlation(signal1, signal2):
    return correlate(signal1, signal2, mode='full')

def time_delay_analysis(signal1, signal2, sampling_period):
    # Calculate cross-correlation
    cross_corr_result = cross_correlation(signal1, signal2)

    # Find the lag with maximum correlation
    max_corr_index = np.argmax(np.abs(cross_corr_result))
    lag = max_corr_index - (len(signal1) - 1)
    lag = lag+1
    # Convert lag to time delay
    time_delay = lag * (1/sampling_period)

    return cross_corr_result, lag, time_delay


def plot_signals_and_correlation(signal1, signal2, cross_corr_result, lag):
    # Plot signals
    plt.subplot(3, 1, 1)
    plt.plot(signal1, label='Signal 1')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(signal2, label='Signal 2')
    plt.legend()

    # Plot cross-correlation
    time_lags = np.arange(-len(signal1) + 1, len(signal2))
    plt.subplot(3, 1, 3)
    plt.plot(time_lags, cross_corr_result, label='Cross-Correlation')
    plt.axvline(x=lag, color='r', linestyle='--', label='Max Correlation Lag')
    plt.legend()

    plt.show()

def browse_file(file_path_var):
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        file_path_var.set(filename)

def process_files(file_path_var1, file_path_var2, sampling_period_var):
    try:
        # Read signals from files
        signal_data1 = read_signal_file(file_path_var1.get())
        signal_data2 = read_signal_file(file_path_var2.get())

        # Extract samples
        samples_signal1 = signal_data1[:, 1]
        samples_signal2 = signal_data2[:, 1]

        # Get sampling period
        sampling_period = float(sampling_period_var.get())

        # Compute time delay analysis
        cross_corr_result, lag, time_delay = time_delay_analysis(samples_signal1, samples_signal2, sampling_period)

        # Display results
        print(f"Estimated Lag: {lag}")
        print(f"Estimated Time Delay: {time_delay} seconds")

        # Plot signals and cross-correlation
        plot_signals_and_correlation(samples_signal1, samples_signal2, cross_corr_result, lag)

    except Exception as e:
        print(f"Error processing files: {e}")

def create_gui():
    root = tk.Tk()
    root.title("Time Delay Analysis with Cross-Correlation")
    root.geometry("600x400")

    file_path_var1 = tk.StringVar()
    file_path_var2 = tk.StringVar()
    sampling_period_var = tk.StringVar()

    file_frame = tk.Frame(root)
    file_frame.pack()

    file_label1 = tk.Label(file_frame, text="Choose Signal File 1:")
    file_label1.grid(row=0, column=0)

    file_entry1 = tk.Entry(file_frame, textvariable=file_path_var1, state='disabled', width=40)
    file_entry1.grid(row=0, column=1)

    file_button1 = tk.Button(file_frame, text="Browse", command=lambda: browse_file(file_path_var1))
    file_button1.grid(row=0, column=2)

    file_label2 = tk.Label(file_frame, text="Choose Signal File 2:")
    file_label2.grid(row=1, column=0)

    file_entry2 = tk.Entry(file_frame, textvariable=file_path_var2, state='disabled', width=40)
    file_entry2.grid(row=1, column=1)

    file_button2 = tk.Button(file_frame, text="Browse", command=lambda: browse_file(file_path_var2))
    file_button2.grid(row=1, column=2)

    sampling_label = tk.Label(file_frame, text="Enter Sampling Period:")
    sampling_label.grid(row=2, column=0)

    sampling_entry = tk.Entry(file_frame, textvariable=sampling_period_var, width=10)
    sampling_entry.grid(row=2, column=1)

    process_button = tk.Button(root, text="Process Signals", command=lambda: process_files(file_path_var1, file_path_var2, sampling_period_var))
    process_button.pack(pady=10)

    root.mainloop()

# Run the GUI
create_gui()
