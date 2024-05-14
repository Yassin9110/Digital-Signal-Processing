import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

from Task6_ConvTest import ConvTest


def perform_conv(x_values1, y_values1, x_values2, y_values2):
    len1 = len(y_values1)
    len2 = len(y_values2)

    start_index = int(min(x_values1) + min(x_values2))
    end_index = int(max(x_values1) + max(x_values2))

    x_values = list(range(start_index, end_index + 1))

    result = [0] * (len1 + len2 - 1)

    for n in range(len1 + len2 - 1):
        for m in range(min(n, len1 - 1) + 1):
            if 0 <= n - m < len2:
                result[n] += y_values1[m] * y_values2[n - m]

    return x_values, result


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
    root.title("Convolution Processor")
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

    process_button = tk.Button(root, text="Process Signals", command=lambda: process_test_files(file_path_var1.get(), file_path_var2.get()))
    process_button.pack(pady=10)

    root.mainloop()


def browse_file(file_path_var):
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        file_path_var.set(filename)


# Run the GUI
create_gui()
