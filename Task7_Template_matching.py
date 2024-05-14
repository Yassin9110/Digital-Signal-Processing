import tkinter as tk
from tkinter import filedialog
import os
import numpy as np


class TemplateMatchingApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x400")
        self.master.title("Template Matching for Signal Classification")
        self.master.configure(bg="white")

        self.test_file_content = None
        self.class1_content = None
        self.class2_content = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Template Matching", font=("Arial", 16), bg="white").pack(pady=10)

        tk.Button(self.master, text="Open Class 1 Folder", command=self.open_class1_folder).pack(pady=10)
        tk.Button(self.master, text="Open Class 2 Folder", command=self.open_class2_folder).pack(pady=10)
        tk.Button(self.master, text="Open Test File", command=self.open_test_file).pack(pady=10)
        tk.Button(self.master, text="Calculate Correlation", command=self.decide_correlation).pack(pady=20)

        self.result_label = tk.Label(self.master, text="", bg="white", font=("Arial", 12))
        self.result_label.pack(pady=10)

    def open_file(self, title):
        file_path = filedialog.askopenfilename(title=f"Select {title} File")
        return self.process_file(file_path)

    def open_folder(self, title):
        folder_path = filedialog.askdirectory(title=f"Select {title} Folder")
        return self.process_folder(folder_path)

    def process_file(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            return np.array(content.split(), dtype=float)

    def process_folder(self, folder_path):
        files_contents = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                content = self.process_file(file_path)
                files_contents.append(content)

        aggregated_samples = self.aggregate_samples(files_contents)
        return aggregated_samples

    def aggregate_samples(self, files_contents):
        max_samples = max(len(content) for content in files_contents)
        aggregated_samples = np.zeros(max_samples)

        for content in files_contents:
            aggregated_samples[:len(content)] += content

        aggregated_samples /= len(files_contents)
        return aggregated_samples

    def calculate_average_correlation(self, test_file_content, folder_content):
        num_samples = min(len(test_file_content), len(folder_content))
        correlation = np.corrcoef(test_file_content[:num_samples], folder_content[:num_samples])[0, 1]
        return correlation

    def open_test_file(self):
        self.test_file_content = self.open_file("Test")

    def open_class1_folder(self):
        self.class1_content = self.open_folder("Class 1")

    def open_class2_folder(self):
        self.class2_content = self.open_folder("Class 2")

    def decide_correlation(self):
        if self.test_file_content is None or self.class1_content is None or self.class2_content is None:
            self.result_label.config(text="Please open all files and folders.")
            return

        correlation_class1 = self.calculate_average_correlation(self.test_file_content, self.class1_content)
        correlation_class2 = self.calculate_average_correlation(self.test_file_content, self.class2_content)

        result_text = f"Average Correlation with Class 1: {correlation_class1:.4f}\nAverage Correlation with Class 2: {correlation_class2:.4f}"

        if correlation_class1 > correlation_class2:
            result_text += "\ndown movement of EOG signal."
        else:
            result_text += "\nup movement of EOG signal"

        self.result_label.config(text=result_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = TemplateMatchingApp(root)
    root.mainloop()
