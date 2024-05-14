import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog

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

    folded_signal = number1[::-1]

    print("Original Signal:")
    print(number1)

    print("\nFolded Signal:")
    print(folded_signal)

    # Plot the original and folded signals
    plt.subplot(2, 1, 1)
    plt.plot(time, number1)
    plt.title('Original Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    plt.subplot(2, 1, 2)
    plt.plot(time, folded_signal)
    plt.title('Folded Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    plt.tight_layout()
    plt.show()

myfram = tk.Tk()
myfram.geometry("400x300")
myfram.title("Folding Signal")
myfram.configure(bg="aquamarine4")

squaring_label = tk.Label(myfram, text="Folding", width=20)
squaring_label.pack(pady=10)

mybutton = tk.Button(myfram, text="Open File", command=open_file, bg="white",
                     fg="black", width=15)
mybutton.pack(padx=20, pady=50)

myfram.mainloop()
