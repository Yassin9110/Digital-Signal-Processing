import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog
from Task5Test import SignalSamplesAreEqual

def open_file():
    filepath1 = filedialog.askopenfilename(title="Select File")
    if filepath1:
        process_signal(filepath1)


def smooth_signal(signal, window_size):
    smoothed_signal = []
    for i in range(len(signal) - window_size + 1):
        window_values = signal[i: i + window_size]
        window_average = sum(window_values) / window_size
        smoothed_signal.append(window_average)
    return np.array(smoothed_signal)


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

    print(smoothed_signal)
    print(len(smoothed_signal))
    #if (window_size == 3):
     #   SignalSamplesAreEqual("D:\Fcis\Year3\DSP\Labs\Tasks\Task6\TestCases\Moving Average\MovAvgTest1.txt",smoothed_signal)
    #elif (window_size == 5):
     #   SignalSamplesAreEqual("D:\Fcis\Year3\DSP\Labs\Tasks\Task6\TestCases\Moving Average\MovAvgTest2.txt",smoothed_signal)

    plt.subplot(2, 1, 1)
    plt.plot(time[:len(smoothed_signal)], smoothed_signal)
    plt.title('Smoothing Signal')
    plt.xlabel('Time')
    plt.ylabel('Smoothed Amplitude')
    plt.tight_layout()
    plt.show()


myfram = tk.Tk()
myfram.geometry("400x300")
myfram.title("Smoothing Signal")
##myfram.configure(bg="aquamarine4")

smoothing_label = tk.Label(myfram, text="Smoothing", width=20)
smoothing_label.pack(pady=10)

mybutton = tk.Button(myfram, text="Open File", command=open_file, bg="white",
                     fg="black", width=15)
mybutton.pack(padx=20, pady=10)

window_size_label = tk.Label(myfram, text="Window Size:")
window_size_label.pack()

window_size_entry = tk.Entry(myfram)
window_size_entry.pack(pady=20)



myfram.mainloop()
