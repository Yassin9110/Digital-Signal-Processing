import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
import os

from P_Task1_test import Compare_Signals
from P_Task_Logic import design_filter, perform_conv, read_file, resample_signal, remove_dc_component, normalize_signal, cross_correlation, normalized_cross_correlation, DCT, calculate_mean_correlation, plot_signal, decide_correlation, read_Test_file


class FIRFilterGUI:
    def __init__(self, master):
        self.ecg_file_path = None
        self.master = master
        master.title("FIR Filter Design")

        # Variables
        self.filter_coefficients = None
        self.x_values1 = None
        self.y_values1 = None
        self.x_values2 = None
        self.y_values2 = None
        self.filter_type = None
        self.FS = None
        self.stop_attenuation = None
        self.fc1 = None
        self.fc2 = None
        self.Transition_band = None

        # File selection
        self.label_filepath = ttk.Label(master, text="Select File:")
        self.label_filepath.grid(row=0, column=0, padx=10, pady=10)

        self.entry_filepath = ttk.Entry(master, width=50)
        self.entry_filepath.grid(row=0, column=1, padx=10, pady=10)

        self.button_browse = ttk.Button(master, text="Browse", command=self.browse_file)
        self.button_browse.grid(row=0, column=2, padx=10, pady=10)

        # Filter parameters
        self.label_filter_type = ttk.Label(master, text="Filter Type:")
        self.label_filter_type.grid(row=1, column=0, padx=10, pady=10)

        self.combo_filter_type = ttk.Combobox(master, values=["Low pass", "High pass", "Band pass", "Band stop"])
        self.combo_filter_type.grid(row=1, column=1, padx=10, pady=10)
        self.combo_filter_type.set("Low pass")
        self.combo_filter_type.bind("<<ComboboxSelected>>", self.update_cutoff_freq2_state)

        self.label_sampling_freq = ttk.Label(master, text="Sampling Frequency:")
        self.label_sampling_freq.grid(row=2, column=0, padx=10, pady=10)

        self.entry_sampling_freq = ttk.Entry(master)
        self.entry_sampling_freq.grid(row=2, column=1, padx=10, pady=10)

        self.label_cutoff_freq = ttk.Label(master, text="Cutoff Frequency:")
        self.label_cutoff_freq.grid(row=3, column=0, padx=10, pady=10)

        self.entry_cutoff_freq = ttk.Entry(master)
        self.entry_cutoff_freq.grid(row=3, column=1, padx=10, pady=10)

        self.label_cutoff_freq2 = ttk.Label(master, text="Cutoff Frequency 2 (for Band pass/Band stop):")
        self.label_cutoff_freq2.grid(row=4, column=0, padx=10, pady=10)

        self.entry_cutoff_freq2 = ttk.Entry(master, state="disabled")
        self.entry_cutoff_freq2.grid(row=4, column=1, padx=10, pady=10)

        self.label_stop_attenuation = ttk.Label(master, text="Stop Attenuation:")
        self.label_stop_attenuation.grid(row=5, column=0, padx=10, pady=10)

        self.entry_stop_attenuation = ttk.Entry(master)
        self.entry_stop_attenuation.grid(row=5, column=1, padx=10, pady=10)

        self.label_transition_band = ttk.Label(master, text="Transition Band:")
        self.label_transition_band.grid(row=6, column=0, padx=10, pady=10)

        self.entry_transition_band = ttk.Entry(master)
        self.entry_transition_band.grid(row=6, column=1, padx=10, pady=10)

        # Process button
        self.button_process = ttk.Button(master, text="Process Filter", command=self.process_filter)
        self.button_process.grid(row=9, column=0, columnspan=1, pady=20)

        # Browse ECG file button
        self.button_browse_ecg = ttk.Button(master, text="Browse ECG File", command=self.browse_ecg_file)
        self.button_browse_ecg.grid(row=10, column=0, columnspan=1, pady=10)

        # Process ECG button
        self.button_process_ecg = ttk.Button(master, text="Process ECG", command=self.process_ecg)
        self.button_process_ecg.grid(row=10, column=0, columnspan=3, pady=10)
        # Resampling parameters
        self.label_resample_factor = ttk.Label(master, text="Resample Factor (M):")
        self.label_resample_factor.grid(row=7, column=0, padx=10, pady=10)

        self.entry_resample_factor = ttk.Entry(master)
        self.entry_resample_factor.grid(row=7, column=1, padx=10, pady=10)

        self.label_resample_length = ttk.Label(master, text="Resample Length (L):")
        self.label_resample_length.grid(row=8, column=0, padx=10, pady=10)

        self.entry_resample_length = ttk.Entry(master)
        self.entry_resample_length.grid(row=8, column=1, padx=10, pady=10)

        # Resample button
        self.button_resample = ttk.Button(master, text="Resample", command=self.run_resample)
        self.button_resample.grid(row=9, column=0, columnspan=3, pady=20)

        # Template matching
        self.label_ecg_match = ttk.Button(master, text="ECG options", command=self.run_template)
        self.label_ecg_match.grid(row=11, column=0, columnspan=3, pady=20)
        

        self.label_FS = ttk.Label(master, text="FS:")
        self.label_FS.grid(row=12, column=0, padx=10, pady=10)
        self.entry_FS = ttk.Entry(master)
        self.entry_FS.grid(row=12, column=1, padx=10, pady=10)

        self.label_miniF = ttk.Label(master, text="mini F:")
        self.label_miniF.grid(row=13, column=0, padx=10, pady=10)
        self.entry_miniF = ttk.Entry(master)
        self.entry_miniF.grid(row=13, column=1, padx=10, pady=10)

        self.label_maxF = ttk.Label(master, text="max F:")
        self.label_maxF.grid(row=14, column=0, padx=10, pady=10)
        self.entry_maxF = ttk.Entry(master)
        self.entry_maxF.grid(row=14, column=1, padx=10, pady=10)

        self.label_newF = ttk.Label(master, text="New F:")
        self.label_newF.grid(row=15, column=0, padx=10, pady=10)
        self.entry_newF = ttk.Entry(master)
        self.entry_newF.grid(row=15, column=1, padx=10, pady=10)




    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.entry_filepath.delete(0, tk.END)
        self.entry_filepath.insert(0, file_path)
        self.load_specs_from_file()

    def load_specs_from_file(self):
        file_path = self.entry_filepath.get()
        try:
            with open(file_path, 'r') as file:
                specs_lines = file.readlines()

            # Display the filter type next to the label
            if specs_lines:
                key, value = map(str.strip, specs_lines[0].split('='))
                if key == "FilterType":
                    self.combo_filter_type.set(value)
                    self.update_gui_elements()

            # Update GUI with loaded specifications
            for line in specs_lines[1:]:
                key, value = map(str.strip, line.split('='))
                try:
                    # Try to convert the value to a float, skip if it's not a numeric value
                    float(value)
                except ValueError:
                    continue

                if key == "FS":
                    self.entry_sampling_freq.delete(0, tk.END)
                    self.entry_sampling_freq.insert(0, value)
                elif key == "StopBandAttenuation":
                    self.entry_stop_attenuation.delete(0, tk.END)
                    self.entry_stop_attenuation.insert(0, value)

                # Check the filter type and adjust GUI elements accordingly
                if self.combo_filter_type.get() in ["Low pass", "High pass"]:
                    if key == "FC":
                        self.entry_cutoff_freq.delete(0, tk.END)
                        self.entry_cutoff_freq.insert(0, value)
                    elif key == "TransitionBand":
                        self.entry_transition_band.delete(0, tk.END)
                        self.entry_transition_band.insert(0, value)
                    # Disable the second cutoff frequency entry for low/high pass
                    self.entry_cutoff_freq2.delete(0, tk.END)
                    self.entry_cutoff_freq2.config(state="disabled")

                elif self.combo_filter_type.get() in ["Band pass", "Band stop"]:
                    if key == "F1":
                        self.entry_cutoff_freq.delete(0, tk.END)
                        self.entry_cutoff_freq.insert(0, value)
                    elif key == "F2":
                        self.entry_cutoff_freq2.delete(0, tk.END)
                        self.entry_cutoff_freq2.insert(0, value)
                    elif key == "TransitionBand":
                        self.entry_transition_band.delete(0, tk.END)
                        self.entry_transition_band.insert(0, value)

            self.update_cutoff_freq2_state()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the file: {e}")

    def update_cutoff_freq2_state(self, event=None):
        filter_type = self.combo_filter_type.get()
        if filter_type in ["Band pass", "Band stop"]:
            self.entry_cutoff_freq2.config(state="normal")
        else:
            self.entry_cutoff_freq2.delete(0, tk.END)
            self.entry_cutoff_freq2.config(state="disabled")

    def update_gui_elements(self):
        filter_type = self.combo_filter_type.get()
        if filter_type in ["Low pass", "High pass"]:
            self.label_cutoff_freq.config(text="Cutoff Frequency:")
            self.label_cutoff_freq2.config(text="")
            self.entry_cutoff_freq2.config(state="disabled")
        elif filter_type in ["Band pass", "Band stop"]:
            self.label_cutoff_freq.config(text="Cutoff Frequency 1:")
            self.label_cutoff_freq2.config(text="Cutoff Frequency 2:")
            self.entry_cutoff_freq2.config(state="normal")

    def process_filter(self):
        # Get parameters from the GUI entry boxes
        filter_type = self.combo_filter_type.get()
        self.filter_type = filter_type

        fs = float(self.entry_sampling_freq.get())
        self.FS = fs

        f1 = float(self.entry_cutoff_freq.get())
        self.fc1 = f1

        f2_entry = self.entry_cutoff_freq2.get()

        # Check if f2 entry is not empty
        if f2_entry:
            f2 = float(f2_entry)
        else:
            # Set a default value or handle it as needed
            f2 = 0.0  # You can adjust this value based on your application logic

        self.fc2 = f2

        delta_s = float(self.entry_stop_attenuation.get())
        self.stop_attenuation = delta_s

        transition_band = float(self.entry_transition_band.get())
        self.Transition_band = transition_band

        # Design FIR filter
        self.x_values2, self.y_values2 = FIRFilterGUI.design_fir_filter(filter_type, fs, f1, f2, delta_s,
                                                                        transition_band)

    def process_ecg(self):
        # Check if filter coefficients are available
        if self.x_values2 is None or self.y_values2 is None:
            messagebox.showerror("Error", "Filter coefficients not available. Please process the filter first.")
            return

        # Read ECG file using the read_file function
        try:
            self.x_values1, self.y_values1 = read_file(self.ecg_file_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reading the ECG file: {e}")
            return

        # Perform convolution
        result = FIRFilterGUI.perform_conv(self.x_values1, self.y_values1, self.x_values2, self.y_values2)

        # Ask user if they want to save the result
        response = messagebox.askyesno("Save Result", "Do you want to save the result?")
        if response:
            self.save_result_to_file(result)

        # Browse and select the test file
        test_file_path = filedialog.askopenfilename(title="Select Test File")
        if not test_file_path:
            return  # User canceled the file selection
        Compare_Signals(test_file_path, result[0], result[1])

    def save_result_to_file(self, result):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    for x_val, y_val in zip(self.x_values1, result):
                        file.write(f"{x_val} {y_val}\n")
                messagebox.showinfo("Success", "Result saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the result: {e}")

    def run_resample(self):
        try:
            M = int(self.entry_resample_factor.get())
            L = int(self.entry_resample_length.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer values for Resample Factor and Resample Length.")
            return

        # Check if filter coefficients are available
        if self.x_values2 is None or self.y_values2 is None:
            messagebox.showerror("Error", "Filter coefficients not available. Please process the filter first.")
            return

        # Check if ECG data is available
        if self.x_values1 is None or self.y_values1 is None:
            messagebox.showerror("Error", "ECG data not available. Please process the ECG first.")
            return

        # Ensure transition_band is specified before calling design_filter
        if self.Transition_band is None:
            messagebox.showerror("Error", "Transition band must be specified.")
            return

        # Resample the signal
        resample_res_x, resample_res_y = resample_signal(
            self.x_values1, self.y_values1, M, L, self.filter_type, self.FS, self.stop_attenuation, self.fc1,
            self.Transition_band
        )

        # Display the length of the resampled signal
        print("The length of resampled x values is:", len(resample_res_x))
        print("The length of resampled y values is:", len(resample_res_y))
        print("The Resampled values are:")
        for x_val, y_val in zip(resample_res_x, resample_res_y):
            print(f"{x_val} {y_val}")

        # Ask user if they want to save the resampled result
        response = messagebox.askyesno("Save Resampled Result", "Do you want to save the resampled result?")
        if response:
            self.save_resampled_result_to_file(resample_res_x, resample_res_y)

        # Browse and select the test file for comparison
        test_file_path = filedialog.askopenfilename(title="Select Test File")
        if not test_file_path:
            return  # User canceled the file selection

        Compare_Signals(test_file_path, resample_res_x, resample_res_y)


    def open_folder(self, title):
        folder_path = filedialog.askdirectory(title=f"Select {title} Folder")
        return self.process_folder(folder_path)
    
    def process_folder(self, folder_path):
        files_contents = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                content = self.process_file(file_path)
                files_contents.append(content)

        samples = self.get_samples(files_contents)
        return samples    
    

    
    def process_file(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            return np.array(content.split(), dtype=float)
        
    def get_samples(self, files_contents):
        max_samples = max(len(content) for content in files_contents)
        get_samples = np.zeros(max_samples)
        print(files_contents)

        for content in files_contents:
            get_samples[:len(content)] += content

        get_samples /= len(files_contents)
        return get_samples
    
    
    
    


    def run_template (self):
        fs = int(self.entry_FS.get())
        minF = int(self.entry_miniF.get())
        maxF = int(self.entry_maxF.get())
        newFs = int(self.entry_newF.get())

        data_A = self.open_folder("A")
        data_B = self.open_folder("B")
        data_x, data_y = read_Test_file()


        plot_signal(data_x, data_y, "Original Signal")

        filter_x, filter_y = design_filter("Band pass", fs, 50, minF, 500, maxF)

        result_x, result_y = perform_conv(data_x, data_y, filter_x, filter_y)
        if newFs >= 2 * fs:
            M = int(newFs / fs)
            L = int(fs / newFs)
            result_x, result_y = resample_signal(result_x, result_y, M, L, 'Low pass', newFs, 50, 0, 500)
        else:
            messagebox.showwarning("Invalid value for newFs")

        # result_x, result_y = resample_signal(result_x, result_y, fs, newFs)

        result_y = remove_dc_component(result_y)

        result_y = normalize_signal(result_y)

        result_y = cross_correlation(result_y, result_y)

        plot_signal(result_x, result_y, "After Auto-correlation")

        result_y = DCT(result_y)

        plot_signal(result_x, result_y, "After DCT")

        template_matching_result = decide_correlation(result_y, data_A, data_B)

        print("Template Matching Result:\n", template_matching_result)

        print("Data A:", data_A)
        print("Data B:", data_B)

        plt.tight_layout()
        plt.show()


    def save_resampled_result_to_file(self, resample_res_x, resample_res_y):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    for x_val, y_val in zip(resample_res_x, resample_res_y):
                        file.write(f"{x_val} {y_val}\n")
                messagebox.showinfo("Success", "Resampled result saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the resampled result: {e}")

    def browse_ecg_file(self):
        self.ecg_file_path = filedialog.askopenfilename()
        # You can display the file path or do other actions as needed

    @staticmethod
    def design_fir_filter(filter_type, fs, f1, f2, delta_s, transition_band):
        x_values2, y_values2 = design_filter(filter_type, fs, delta_s, f1, transition_band, f2)
        return x_values2, y_values2

    @staticmethod
    def perform_conv(x_values1, y_values1, x_values2, y_values2):
        result = perform_conv(x_values1, y_values1, x_values2, y_values2)
        return result
    


    


    
    """
    def resample_signal(self):
     #   try:
      #      M = int(self.entry_resample_factor.get())
       #     L = int(self.entry_resample_length.get())
        #except ValueError:
         #   messagebox.showerror("Error", "Please enter valid integer values for Resample Factor and Resample Length.")
          #  return

     # Check if filter coefficients are available
        if self.x_values2 is None or self.y_values2 is None:
            messagebox.showerror("Error", "Filter coefficients not available. Please process the filter first.")
            return

     # Check if ECG data is available
        if self.x_values1 is None or self.y_values1 is None:
            messagebox.showerror("Error", "ECG data not available. Please process the ECG first.")
            return

     # Ensure transition_band is specified before calling design_filter
        if self.TB is None:
            messagebox.showerror("Error", "Transition band must be specified.")
            return

     # Resample the signal
        resampled_x, resampled_y = resample_signal(
            self.x_values1, self.y_values1, M, L, self.filter_type, self.FS, self.stop_attenuation, self.fc1, self.TB
        )

        # Perform convolution with the resampled signal
        #result = FIRFilterGUI.perform_conv(resampled_x, resampled_y, self.x_values2, self.y_values2)

        # Further processing or visualization can be added here


    """


if __name__ == "__main__":
    root = tk.Tk()
    app = FIRFilterGUI(root)
    root.mainloop()