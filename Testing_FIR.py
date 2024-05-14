import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def design_fir_filter(filter_type, fs, f1, f2, delta_s, transition_band):
    # Normalize frequencies
    f1 /= fs
    f2 /= fs
    transition_band /= fs

    # Adjust frequencies using half transition band
    f1 += 0.5 * transition_band
    f2 -= 0.5 * transition_band

    # Calculate filter order (N)
    N = int(4 / transition_band)

    # Ensure N is odd
    if N % 2 == 0:
        N += 1

    # Choose an appropriate window
    if filter_type == 'low':
        window = np.hamming(N)
        h = np.sinc(2 * f1 * (np.arange(N) - (N - 1) / 2))
    elif filter_type == 'high':
        window = np.hamming(N)
        h = np.sinc(2 * f1 * (np.arange(N) - (N - 1) / 2))
        h = -h
        h[(N - 1) // 2] += 1
    elif filter_type == 'bandpass':
        window = np.hamming(N)
        h = np.sinc(2 * f2 * (np.arange(N) - (N - 1) / 2)) - np.sinc(2 * f1 * (np.arange(N) - (N - 1) / 2))
    elif filter_type == 'bandstop':
        window = np.hamming(N)
        h = np.sinc(2 * f1 * (np.arange(N) - (N - 1) / 2)) - np.sinc(2 * f2 * (np.arange(N) - (N - 1) / 2))
        h[(N - 1) // 2] += 1

    # Apply window function
    h = h * window

    # Normalize coefficients to have unity gain at zero frequency
    h = h / np.sum(h)

    return h

def apply_filter(input_signal, filter_coefficients):
    output_signal = convolve(input_signal, filter_coefficients, mode='same')
    return output_signal

def plot_signals(input_signal, output_signal):
    plt.figure(figsize=(12, 6))
    plt.plot(input_signal, label='Input Signal')
    plt.plot(output_signal, label='Filtered Signal')
    plt.legend()
    plt.title('Input and Filtered Signals')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.show()

def save_coefficients(filter_coefficients, filename):
    np.savetxt(filename, filter_coefficients, delimiter=',')

def show_file_values(filepath):
    try:
        input_signal = np.loadtxt(filepath, delimiter=',')
        return input_signal
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the file: {e}")
        return None

def edit_file_values(values):
    root = tk.Tk()
    root.title("Edit File Values")

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, padx=10, pady=10)

    text = tk.Text(frame, wrap=tk.WORD, height=15, width=30)
    text.insert(tk.END, "\n".join(map(str, values)))
    text.grid(row=0, column=0)

    scrollbar = ttk.Scrollbar(frame, command=text.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    text['yscrollcommand'] = scrollbar.set

    button_save = ttk.Button(root, text="Save Changes", command=lambda: save_changes(text.get("1.0", tk.END), root))
    button_save.grid(row=1, column=0, pady=10)

    root.mainloop()

def save_changes(new_values, root):
    try:
        edited_values = np.fromstring(new_values, sep='\n')
        messagebox.showinfo("Success", "Changes saved successfully!")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving changes: {e}")

def browse_file():
    file_path = filedialog.askopenfilename()
    entry_filepath.delete(0, tk.END)
    entry_filepath.insert(0, file_path)

    file_values = show_file_values(file_path)
    if file_values is not None:
        edit_choice = messagebox.askyesno("Edit File Values", "Do you want to edit the file values?")
        if edit_choice:
            edit_file_values(file_values)

def process_filter():
    input_filepath = entry_filepath.get()
    try:
        input_signal = np.loadtxt(input_filepath, delimiter=',')  # Assuming the file contains the input signal
        filter_type = combo_filter_type.get()
        fs = float(entry_sampling_freq.get())
        f1 = float(entry_cutoff_freq.get())
        f2 = float(entry_cutoff_freq2.get())
        delta_s = float(entry_stop_attenuation.get())
        transition_band = float(entry_transition_band.get())

        filter_coefficients = design_fir_filter(filter_type, fs, f1, f2, delta_s, transition_band)
        filtered_signal = apply_filter(input_signal, filter_coefficients)
        plot_signals(input_signal, filtered_signal)

        save_coefficients(filter_coefficients, 'filter_coefficients.txt')
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI setup
root = tk.Tk()
root.title("FIR Filter Design")

# File selection
label_filepath = ttk.Label(root, text="Select File:")
label_filepath.grid(row=0, column=0, padx=10, pady=10)
entry_filepath = ttk.Entry(root, width=50)
entry_filepath.grid(row=0, column=1, padx=10, pady=10)
button_browse = ttk.Button(root, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2, padx=10, pady=10)

# Filter parameters
label_filter_type = ttk.Label(root, text="Filter Type:")
label_filter_type.grid(row=1, column=0, padx=10, pady=10)
combo_filter_type = ttk.Combobox(root, values=["low", "high", "bandpass", "bandstop"])
combo_filter_type.grid(row=1, column=1, padx=10, pady=10)
combo_filter_type.set("low")

label_sampling_freq = ttk.Label(root, text="Sampling Frequency:")
label_sampling_freq.grid(row=2, column=0, padx=10, pady=10)
entry_sampling_freq = ttk.Entry(root)
entry_sampling_freq.grid(row=2, column=1, padx=10, pady=10)

label_cutoff_freq = ttk.Label(root, text="Cutoff Frequency:")
label_cutoff_freq.grid(row=3, column=0, padx=10, pady=10)
entry_cutoff_freq = ttk.Entry(root)
entry_cutoff_freq.grid(row=3, column=1, padx=10, pady=10)

label_cutoff_freq2 = ttk.Label(root, text="Cutoff Frequency 2 (for bandpass/bandstop):")
label_cutoff_freq2.grid(row=4, column=0, padx=10, pady=10)
entry_cutoff_freq2 = ttk.Entry(root)
entry_cutoff_freq2.grid(row=4, column=1, padx=10, pady=10)

label_stop_attenuation = ttk.Label(root, text="Stop Attenuation:")
label_stop_attenuation.grid(row=5, column=0, padx=10, pady=10)
entry_stop_attenuation = ttk.Entry(root)
entry_stop_attenuation.grid(row=5, column=1, padx=10, pady=10)

label_transition_band = ttk.Label(root, text="Transition Band:")
label_transition_band.grid(row=6, column=0, padx=10, pady=10)
entry_transition_band = ttk.Entry(root)
entry_transition_band.grid(row=6, column=1, padx=10, pady=10)

# Process button
button_process = ttk.Button(root, text="Process Filter", command=process_filter)
button_process.grid(row=7, column=0, columnspan=3, pady=20)

root.mainloop()
