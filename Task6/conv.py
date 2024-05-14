import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

def open_file():
    global filepath1
    filepath1 = filedialog.askopenfilename(title="Select File 1")
    if filepath1:
        if 'filepath2' in globals():
            process_signals(filepath1, filepath2)
        else:
            print("Please select the second file.")

def open_file2():
    global filepath2
    filepath2 = filedialog.askopenfilename(title="Select File 2")
    if filepath2:
        if 'filepath1' in globals():
            process_signals(filepath1, filepath2)
        else:
            print("Please select the first file.")

def process_signals(filepath1, filepath2):
    if 'filepath1' not in globals() or 'filepath2' not in globals():
        print("Please select both files.")
        return

    # Load data for Signal 1
    with open(filepath1, 'r') as file1:
        lines1 = file1.read().splitlines()

    # Process data for Signal 1
    data1 = [list(map(float, line.split())) for line in lines1[3:]]
    time1, signal1 = zip(*data1)

    # Load data for Signal 2
    with open(filepath2, 'r') as file2:
        lines2 = file2.read().splitlines()

    # Process data for Signal 2
    data2 = [list(map(float, line.split())) for line in lines2[3:]]
    time2, signal2 = zip(*data2)

    # Convolve the two signals
    convolution_result = convolution(signal1, signal2)

    # Plot the original signals and the convolution result
    plt.subplot(3, 1, 1)
    plt.stem(time1, signal1, basefmt='b-')
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

def convolution(signal1, signal2):
    len_result = len(signal1) + len(signal2) - 1
    result = [0] * len_result

    for i in range(len(signal1)):
        for j in range(len(signal2)):
            result[i + j] += signal1[i] * signal2[j]

    return result

myfram = tk.Tk()
myfram.geometry("400x300")
myfram.title("Choose Files and Convolve")
myfram.configure(bg="palegreen4")

mybutton = tk.Button(myfram, text="Open File 1", command=open_file, bg="black", fg="white")
mybutton.pack(side="left", padx=40)

mybutton2 = tk.Button(myfram, text="Open File 2", command=open_file2, bg="white", fg="black")
mybutton2.pack(side="right", padx=40)

myfram.mainloop()
