import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np

from Task6_ConvTest import ConvTest
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

def fast_correlation(x1, x2):
    N = len(x1)

    # Use the fast Fourier transform (FFT)
    X1 = np.fft.fft(x1)
    X2 = np.fft.fft(x2)

    # Compute the cross-correlation in the frequency domain
    fast_corr_result = np.fft.ifft(X1 * np.conj(X2))

    # Normalize the result
    #fast_corr_result /= np.sqrt(np.sum(np.abs(x1) ** 2) * np.sum(np.abs(x2) ** 2))

    print("Corr result is: ", np.real(fast_corr_result))

    return np.real(fast_corr_result)

def perform_conv(x_values1, y_values1, x_values2, y_values2):
    len1 = len(y_values1)
    len2 = len(y_values2)

    start_index = int(min(x_values1) + min(x_values2))
    end_index = int(max(x_values1) + max(x_values2))

    x_values = list(range(start_index, end_index + 1))

    padded_len = 2**int(np.ceil(np.log2(len1 + len2 - 1)))
    fft_y1 = np.fft.fft(y_values1, padded_len)
    fft_y2 = np.fft.fft(y_values2, padded_len)

    result = np.fft.ifft(fft_y1 * fft_y2).real


    print("RES indices is: ", x_values)
    print("Conv result is: ", result)

    return x_values, result[:len(x_values)]

def process_files(file_path1, file_path2):
    # Read signals from files
    signal_data1 = read_signal_file(file_path1)
    signal_data2 = read_signal_file(file_path2)

    # Extract samples
    samples_signal1 = signal_data1[:, 1]
    samples_signal2 = signal_data2[:, 1]

    # Compute fast cross-correlation
    fast_corr_result = fast_correlation(samples_signal1, samples_signal2)
    indices = np.arange(len(fast_corr_result))

    # Display the result and plot the signals
    print("Fast Correlation Result:")
    for i, value in enumerate(fast_corr_result):
        print(f"{i} {value}")

    Compare_Signals("Task8\Correlation\CorrOutput.txt", indices, fast_corr_result)

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
    plt.plot(indices, fast_corr_result, label='Fast Correlation')
    plt.title('Fast Correlation Result')
    plt.xlabel('Index')
    plt.ylabel('Correlation Value')
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_convolution(x_values1, y_values1, x_values2, y_values2, x_result, result):
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(x_values1, y_values1, label='Signal 1')
    plt.title('Signal 1')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(x_values2, y_values2, label='Signal 2')
    plt.title('Signal 2')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(x_result, result, label='Convolution Result', color='red')
    plt.title('Convolution Result')
    plt.legend()

    plt.show()

def process_test_files(file_path1, file_path2):
    x_values1, y_values1 = read_file(file_path1)
    x_values2, y_values2 = read_file(file_path2)

    x_values, result = perform_conv(x_values1, y_values1, x_values2, y_values2)

    ConvTest(x_values, result)

    plot_convolution(x_values1, y_values1, x_values2, y_values2, x_values, result)

def read_file(file_path):
    x_values = []
    y_values = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[3:]:
            values = line.strip().split()
            x_values.append(float(values[0]))
            y_values.append(float(values[1]))

    return x_values, y_values

# GUI setup
def create_gui():
    root = tk.Tk()
    root.title("Fast Operation Calculator")
    root.geometry("350x150")
    header_label = tk.Label(root, text= "FINALLY LAST TASK!!")
    header_label.pack(side='top')


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

    process_corr_button = tk.Button(root, text="Process Correlation", command=lambda: process_files(file_path_var1.get(), file_path_var2.get()))
    process_corr_button.pack(pady=5)

    process_conv_button = tk.Button(root, text="Process Convolution", command=lambda: process_test_files(file_path_var1.get(), file_path_var2.get()))
    process_conv_button.pack(pady=5)
    
    root.mainloop()

def browse_file(file_path_var):
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        file_path_var.set(filename)

# Run the GUI
create_gui()
