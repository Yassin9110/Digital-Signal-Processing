import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np

def open_file():
    filepath1 = filedialog.askopenfilename(title="Select File")
    if filepath1:
        process_signal(filepath1)

def process_signal(filepath1):
    with open(filepath1, 'r') as file1:
        lines1 = file1.read().splitlines()

    data1 = [line.split() for line in lines1[3:]]
    data1 = np.array(data1, dtype=float)

    time = np.arange(0, len(data1))

    number1 = data1[:, 1]

    # Get window size from user input in GUI
    window_size = int(window_size_entry.get())

    smoothed_signal = smooth_signal(number1, window_size)
    delayed_signal = delay_signal(number1, int(entry_k.get()))
    folded_signal = fold_signal(number1)
    shifted_folded_signal = shift_fold_signal(number1, window_size)

    plot_signal(time, number1, smoothed_signal, title='Original vs. Smoothed Signal')
    plot_signal(time, number1, delayed_signal, title='Original vs. Delayed/Advanced Signal')
    plot_signal(time, number1, folded_signal, title='Original vs. Folded Signal')
    plot_signal(time[:len(smoothed_signal)], smoothed_signal, title='Smoothed Signal')

    # Display the Convolution button
    convolution_button.pack()

def smooth_signal(signal, window_size):
    smoothed_signal = []
    for i in range(len(signal) - window_size + 1):
        window_values = signal[i: i + window_size]
        window_average = sum(window_values) / window_size
        smoothed_signal.append(window_average)
    return np.array(smoothed_signal)

def delay_signal(signal, k):
    delayed_signal = np.zeros_like(signal)
    delayed_signal[k:] = signal[:-k]
    return delayed_signal

def fold_signal(signal):
    return signal[::-1]

def shift_fold_signal(signal, window_size):
    smoothed_signal = smooth_signal(signal, window_size)
    return fold_signal(smoothed_signal)

def plot_signal(time, *signals, title=''):
    plt.figure()
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    for i, signal in enumerate(signals):
        plt.plot(time[:len(signal)], signal, label=f'Signal {i + 1}')

    plt.legend()
    plt.tight_layout()
    plt.show()

def convolution():
    global filepath2
    filepath2 = filedialog.askopenfilename(title="Select File 2")
    if filepath2:
        process_convolution(filepath2)

def process_convolution(filepath2):
    if 'filepath1' not in globals():
        print("Please select the first file.")
        return

    # Load data for Signal 2
    with open(filepath2, 'r') as file2:
        lines2 = file2.read().splitlines()

    # Process data for Signal 2
    data2 = [list(map(float, line.split())) for line in lines2[3:]]
    time2, signal2 = zip(*data2)

    # Convolve the two signals
    convolution_result = convolution_signal(number1, signal2)

    # Plot the original signals and the convolution result
    plt.subplot(3, 1, 1)
    plt.stem(time, number1, basefmt='b-')
    plt.title('Signal 1')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    plt.subplot(3, 1, 2)
    plt.stem(time2, signal2, basefmt='r-')
    plt.title('Signal 2')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    plt.subplot(3, 1, 3)
    plt.stem(convolution_result, basefmt='g-')
    plt.title('Convolution Result')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    plt.tight_layout()
    plt.show()

def convolution_signal(signal1, signal2):
    len_result = len(signal1) + len(signal2) - 1
    result = np.convolve(signal1, signal2, mode='full')
    return result

myfram = tk.Tk()
myfram.geometry("400x500")
myfram.title("Signal Processing")
myfram.configure(bg="palegreen4")

# Buttons for operations
smoothing_button = tk.Button(myfram, text="Smoothing", command=open_file, bg="white", fg="black", width=15)
smoothing_button.pack(pady=10)

label_k = tk.Label(myfram, text="Enter k:", width=20)
label_k.pack(pady=5)

entry_k = tk.Entry(myfram, width=10)
entry_k.pack(pady=5)

shifting_button = tk.Button(myfram, text="Shift Signal", command=open_file, bg="white", fg="black", width=15)
shifting_button.pack(pady=10)

folding_button = tk.Button(myfram, text="Fold Signal", command=open_file, bg="white", fg="black", width=15)
folding_button.pack(pady=10)

shift_fold_button = tk.Button(myfram, text="Shift and Fold", command=open_file, bg="white", fg="black", width=15)
shift_fold_button.pack(pady=10)

# Entry for window size
window_size_label = tk.Label(myfram, text="Window Size:")
window_size_label.pack()

window_size_entry = tk.Entry(myfram)
window_size_entry.pack(pady=20)

# Convolution button (hidden initially)
convolution_button = tk.Button(myfram, text="Convolution", command=convolution, bg="white", fg="black", width=15)

myfram.mainloop()
