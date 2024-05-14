import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import os

def open_file(file_listbox, file_list):
    file_path = filedialog.askopenfilename(filetypes=[("Signal files", "*.txt")])
    if file_path:
        file_list.append(file_path)
        file_listbox.insert(tk.END, os.path.basename(file_path))
        print("Added:", file_path)

def remove_file(file_listbox, file_list):
    selected_index = file_listbox.curselection()
    if selected_index:
        file_path = file_list.pop(selected_index[0])
        file_listbox.delete(selected_index)
        print("Removed:", file_path)

def clear_files(file_listbox, file_list):
    file_listbox.delete(0, tk.END)
    file_list.clear()
    print("Cleared all files")

def shift_signal(file_listbox, file_list, shift_entry):
    selected_index = file_listbox.curselection()
    if selected_index:
        file_path = file_list[selected_index[0]]
        try:
            shift_value = float(shift_entry.get())
            data = np.genfromtxt(file_path, skip_header=3)
            time, amplitude = data[:, 0], data[:, 1]
            shifted_time, shifted_amplitude = time + shift_value, amplitude

            filename = os.path.basename(file_path)
            fig, ax = plt.subplots()
            ax.plot(time, amplitude, label=f"{filename} (Original)")
            ax.plot(shifted_time, shifted_amplitude, label=f"{filename} (Shifted)")
            ax.set_xlabel('Time (t)')
            ax.set_ylabel('Amplitude')
            ax.set_title('Resulting Signal (Shifted)')
            ax.legend()
            plt.show()
        except ValueError:
            print("Error: Please enter a valid numeric shift value.")
    else:
        print("Error: Please select a file to shift.")

# Create the main window
window = tk.Tk()
window.title("Shift Signal")

# Create the file selection widgets
file_list = []
file_label = tk.Label(window, text="Select Signal File:")
file_label.grid(row=0, column=0, padx=5, pady=5)

file_listbox = tk.Listbox(window, width=50)
file_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

add_file_button = tk.Button(window, text="Add File", command=lambda: open_file(file_listbox, file_list))
add_file_button.grid(row=2, column=0, padx=5, pady=5)

remove_file_button = tk.Button(window, text="Remove File", command=lambda: remove_file(file_listbox, file_list))
remove_file_button.grid(row=2, column=1, padx=5, pady=5)

clear_files_button = tk.Button(window, text="Clear Files", command=lambda: clear_files(file_listbox, file_list))
clear_files_button.grid(row=2, column=2, padx=5, pady=5)

# Shift value entry
shift_label = tk.Label(window, text="Shift Value:")
shift_label.grid(row=3, column=0, padx=5, pady=5)

shift_entry = tk.Entry(window)
shift_entry.grid(row=3, column=1, padx=5, pady=5)

shift_button = tk.Button(window, text="Shift", command=lambda: shift_signal(file_listbox, file_list, shift_entry))
shift_button.grid(row=3, column=2, padx=5, pady=5)

# Start the GUI
window.mainloop()
