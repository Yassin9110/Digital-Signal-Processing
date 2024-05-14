from tkinter import *
from tkinter import filedialog
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Task8_ConvTest import ConvTest
from Task8_CompareSignal import Compare_Signals

def open_file():
    file_path = filedialog.askopenfilename()
    x_values = []
    y_values = []

    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines[3:]:
                values = line.strip().split()
                x_values.append(float(values[0]))
                y_values.append(float(values[1]))

    return x_values, y_values

def DFT(signal):
    N = len(signal)
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        X[k] = 0
        for n in range(N):
            X[k] += signal[n] * np.exp(-2j * np.pi * k * n / N)

    return X

def IDFT(X):
    N = len(X)
    signal = np.zeros(N, dtype=complex)

    for n in range(N):
        signal[n] = 0
        for k in range(N):
            angle = 2 * np.pi * n * k / N
            real_part = np.cos(angle)
            imaginary_part = np.sin(angle)
            signal[n] += (X[k].real * real_part) - (X[k].imag * imaginary_part)

        signal[n] /= N

    return signal

def fast_cross_correlation(x1, x2):
    N = len(x1)
    X1 = DFT(x1)
    X2 = DFT(x2)
    X1_conj = np.conjugate(X1)
    result_conj = X1_conj * X2
    result = IDFT(result_conj) / N

    x_values_result = np.arange(0, N)

    # print (x_values_result)
    # print (fast_corr_result.real*2/N)
    Compare_Signals("Fast_Correlation/Corr_Output.txt", x_values_result,result.real)

    return result.real

# Task 2
def fast_correlation(x1, x2):
    N = len(x1)

    X1 = DFT(x1)
    X2 = DFT(x2)

    fast_corr_result = IDFT(X1 * np.conj(X2))
    fast_corr_result*= 2/N

    x_values_result = np.arange(0, N)

    # print (x_values_result)
    # print (fast_corr_result.real*2/N)
    Compare_Signals("Fast_Correlation/Corr_Output.txt", x_values_result,fast_corr_result.real*2/N)

    return fast_corr_result.real*2/N

# Task 1
def convolution(x_values1, y_values1, x_values2, y_values2):
    len1 = len(y_values1)
    len2 = len(y_values2)

    extended_len = len1 + len2 - 1
    y_values1_padded = np.pad(y_values1, (0, extended_len - len1))
    y_values2_padded = np.pad(y_values2, (0, extended_len - len2))

    Y1 = DFT(y_values1_padded)
    Y2 = DFT(y_values2_padded)

    result_freq_domain = Y1 * Y2

    result_time_domain = IDFT(result_freq_domain)

    start_index = int(min(x_values1))
    x_values_result = np.arange(start_index, start_index + extended_len)

    ConvTest(x_values_result, result_time_domain.real)

    return x_values_result, result_time_domain.real

def plot_signals(x1, y1, x2, y2, result_x, result, operation):
    fig, ax = plt.subplots(3, 1, figsize=(8, 6))

    ax[0].plot(x1, y1, label='Signal 1')
    ax[0].set_title('Signal 1')

    ax[1].plot(x2, y2, label='Signal 2')
    ax[1].set_title('Signal 2')

    ax[2].plot(result_x, result, label=f'{operation} Result', color='red')
    ax[2].set_title(f'{operation} Result')

    for axis in ax:
        axis.legend()
        axis.grid(True)

    plt.tight_layout()
    plt.show()

class SignalConvolutionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Signal Convolution App")

        self.x1_button = Button(self.master, text="Load Signal 1", command=self.load_x1)
        self.x1_button.pack()

        self.signal2_button = Button(self.master, text="Load Signal 2", command=self.load_signal2)
        self.signal2_button.pack()

        self.convolve_button = Button(self.master, text="Perform Convolution", command=self.perform_convolution)
        self.convolve_button.pack()

        self.autocorr_button = Button(self.master, text="Perform Autocorrelation", command=self.perform_autocorrelation)
        self.autocorr_button.pack()

    def load_x1(self):
        self.x_values1, self.y_values1 = open_file()

    def load_signal2(self):
        self.x_values2, self.y_values2 = open_file()

    def perform_convolution(self):
        x_result, result = convolution(self.x_values1, self.y_values1, self.x_values2, self.y_values2)
        plot_signals(self.x_values1, self.y_values1, self.x_values2, self.y_values2, x_result, result, "Fast-Convolution")

    def perform_autocorrelation(self):
        autocorr_result = fast_cross_correlation(self.y_values1, self.y_values2)
        plot_signals(self.x_values1, self.y_values1, [], [], np.arange(len(autocorr_result)), autocorr_result, "Fast-Correlation")

if __name__ == "__main__":
    root = Tk()
    app = SignalConvolutionApp(root)
    root.mainloop()