import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt


def calculate_window_type(stop_band_attenuation):
    if stop_band_attenuation <= 21:
        return "rectangular"
    elif stop_band_attenuation <= 44:
        return "hanning"
    elif stop_band_attenuation <= 53:
        return "hamming"
    elif stop_band_attenuation <= 74:
        return "blackman"
    else:
        raise ValueError("Stop band attenuation is too high. Choose a lower value.")


def window_function(window_type, n, N):
    if window_type == "rectangular":
        return 1
    elif window_type == "hanning":
        return 0.5 + (0.5 * np.cos((2 * np.pi * n) / N))
    elif window_type == "hamming":
        return 0.54 + (0.46 * np.cos((2 * np.pi * n) / N))
    elif window_type == "blackman":
        return 0.42 + (0.5 * np.cos(2 * np.pi * n / (N - 1))) + 0.08 * np.cos(4 * np.pi * n / (N - 1))


def calculate_samples(window_type, delta_f):
    if window_type == "rectangular":
        return int(np.ceil(0.9 / delta_f))
    elif window_type == "hanning":
        return int(np.ceil(3.1 / delta_f))
    elif window_type == "hamming":
        return int(np.ceil(3.3 / delta_f))
    elif window_type == "blackman":
        return int(np.ceil(5.5 / delta_f))


def design_filter(filter_type, FS, stop_band_attenuation, FC, transition_band, FC2=None, ):
    window_type = calculate_window_type(stop_band_attenuation)
    print("The window type is:", window_type)

    if filter_type not in ["Low pass", "High pass", "Band pass", "Band stop"]:
        raise ValueError("Invalid filter type. Choose from 'low_pass', 'high_pass', 'band_pass', or 'band_reject'.")

    if window_type not in ["rectangular", "hanning", "hamming", "blackman"]:
        raise ValueError("Invalid window type. Choose from 'rectangular', 'hanning', 'hamming', or 'blackman'.")

    delta_f = transition_band / FS
    N = calculate_samples(window_type, delta_f)
    if N % 2 == 0:
        N += 1
    print("N=", N)

    if filter_type == "Low pass":
        new_fc = FC + 0.5 * transition_band
        print("fc=", new_fc)
        new_fc = new_fc / FS
        print("The normalized fc=", new_fc)

    elif filter_type == "High pass":
        new_fc = FC - 0.5 * transition_band
        print("fc=", new_fc)
        new_fc = new_fc / FS
        print("The normalized fc=", new_fc)

    elif filter_type == "Band pass":
        new_fc = FC - 0.5 * transition_band
        print("fc1=", new_fc)
        new_fc = new_fc / FS
        print("The normalized fc1=", new_fc)
        if FC2 is None:
            raise ValueError("For band pass or, FC2 must be specified.")
        new_fc2 = FC2 + 0.5 * transition_band
        print("fc2=", new_fc2)
        new_fc2 = new_fc2 / FS
        print("The normalized fc2=", new_fc2)

    elif filter_type == "Band stop":
        new_fc = FC + 0.5 * transition_band
        print("fc1=", new_fc)
        new_fc = new_fc / FS
        print("The normalized fc1=", new_fc)
        if FC2 is None:
            raise ValueError("For band reject, FC2 must be specified.")
        new_fc2 = FC2 - 0.5 * transition_band
        print("fc2=", new_fc2)
        new_fc2 = new_fc2 / FS
        print("The normalized fc2=", new_fc2)

    # Create the filter
    h = []

    for i in range(-N // 2 + 1, N // 2 + 1):
        n = i

        if filter_type == "Low pass":
            if i == 0:
                h.append(2 * new_fc)
            else:
                sinc_term = (
                    ((2 * new_fc * np.sin(n * 2 * np.pi * new_fc)) / (n * 2 * np.pi * new_fc)))
                h_value = sinc_term * window_function(window_type, n, N)
                h.append(h_value)

        elif filter_type == "High pass":
            if i == 0:
                h_value = (1 - 2 * new_fc) * window_function(window_type, n, N)
                h.append(h_value)
            else:
                sinc_term = (
                    ((2 * new_fc * np.sin(n * 2 * np.pi * new_fc)) / (n * 2 * np.pi * new_fc)))
                h_value = -(sinc_term * window_function(window_type, n, N))
                h.append(h_value)

        elif filter_type == "Band pass":
            if i == 0:
                h_value = (2 * (new_fc2 - new_fc)) * window_function(window_type, n, N)
                h.append(h_value)
            else:
                sinc_term1 = (
                    ((2 * new_fc * np.sin(n * 2 * np.pi * new_fc)) / (n * 2 * np.pi * new_fc)))
                sinc_term2 = (((2 * new_fc2 * np.sin(n * 2 * np.pi * new_fc2)) / (
                        n * 2 * np.pi * new_fc2)))
                total_sincs = sinc_term2 - sinc_term1
                h_value = total_sincs * window_function(window_type, n, N)
                h.append(h_value)

        elif filter_type == "Band stop":
            if i == 0:
                h_value = (1 - (2 * (new_fc2 - new_fc))) * window_function(window_type, n, N)
                h.append(h_value)
            else:
                sinc_term1 = (
                    ((2 * new_fc * np.sin(n * 2 * np.pi * new_fc)) / (n * 2 * np.pi * new_fc)))
                sinc_term2 = (((2 * new_fc2 * np.sin(n * 2 * np.pi * new_fc2)) / (
                        n * 2 * np.pi * new_fc2)))
                total_sincs = sinc_term1 - sinc_term2
                h_value = total_sincs * window_function(window_type, n, N)
                h.append(h_value)

    # Print the indices and corresponding values
    x_values = []
    for i in range(-N // 2 + 1, N // 2 + 1):
        n = i
        x_values.append(n)
        print(f"{n} {h[i + N // 2]}")

    # Plot the filter response
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, h, label=f'{filter_type} Filter Response')
    plt.title('Filter Response')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

    return x_values, h


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


def read_Test_file ():

        file_path = filedialog.askopenfilename()
        x_values = []
        y_values = []

        if file_path:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines[3:]:
                    values = line.strip().split()
                    # x_values.append(float(values[0]))
                    y_values.append(float(values[0]))

        x_values = range(len(y_values))

        return x_values, y_values




def perform_conv(x_values1, y_values1, x_values2, y_values2):
    len1 = len(y_values1)
    len2 = len(y_values2)

    print("The length of signal =", len1)
    print("The length of filter =", len2)

    x_values_Lenght = len1 + len2 - 1
    print("The length of filtered signal =", x_values_Lenght)

    result = [0] * x_values_Lenght  # Initialize the result list with zeros

    x_values = []  # Initialize the list to store x values

    for n in range(x_values_Lenght):
        x_values.append(n - len2 // 2)  # Store the x values

        for m in range(min(n, len1 - 1) + 1):
            if 0 <= n - m < len2:
                result[n] += y_values1[m] * y_values2[n - m]

    print("Index (x values) and Corresponding Results:")
    for x_val, res in zip(x_values, result):
        print(f"{x_val} {res}")

    # Plot the convolution result
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, result, label='Convolution Result')
    plt.title('Convolution Result')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

    return x_values, result


def upsample(signal, factor):
    result = []
    for element in signal:
        result.extend([element] + [0] * (factor - 1))
    for i in range(factor - 1):
        result.pop()
    return result


def resample_signal(input_x, input_y, M, L, filter_type, fs, stop_band_attenuation, fc, transition_band):
    if M == 0 and L != 0:
        # Upsample by inserting L-1 zeros between each sample
        upsampled_signal = upsample(input_y, L)
        filtered_x, filtered_y = design_filter(filter_type, fs, stop_band_attenuation, fc, transition_band)
        result_x, result_y = perform_conv(input_x, upsampled_signal, filtered_x, filtered_y)

        # Plot the results
        plt.plot(result_x, result_y)
        plt.title('Upsample and Filter')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.show()

        return result_x, result_y

    elif M != 0 and L == 0:
        # Downsample by taking every Mth sample
        filtered_x, filtered_y = design_filter(filter_type, fs, stop_band_attenuation, fc, transition_band)
        output_x, output_y = perform_conv(input_x, input_y, filtered_x, filtered_y)
        output_x, output_y = output_x[::M], output_y[::M]
        continuous_indices = list(range(min(output_x), min(output_x) + len(output_x)))
        # Plot the results
        plt.plot(continuous_indices, output_y)
        plt.title('Downsample and Filter')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.show()

        return continuous_indices, output_y

    elif M != 0 and L != 0:
        # Upsample, filter, and then downsample
        upsampled_signal = upsample(input_y, L)
        upsampled_x = upsample(input_x, L)
        upsampled_x = list(range(int(min(upsampled_x)), int(min(upsampled_x)) + len(upsampled_x)))
        filtered_x, filtered_y = design_filter(filter_type, fs, stop_band_attenuation, fc, transition_band)
        filtered_signal_x, filtered_signal_y = perform_conv(upsampled_x, upsampled_signal, filtered_x, filtered_y)
        filtered_signal_x, filtered_signal_y = filtered_signal_x[::M], filtered_signal_y[::M]
        continuous_indices = list(range(min(filtered_signal_x), min(filtered_signal_x) + len(filtered_signal_x)))
        # Plot the results
        plt.plot(continuous_indices, filtered_signal_y)
        plt.title('Upsample, Filter, and Downsample')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.show()

        return continuous_indices, filtered_signal_y

    else:
        messagebox.showerror("Error", "Invalid values for M and L. Please provide non-zero values for either M or L.")
        return None, None



def remove_dc_component(x):
    return x - np.mean(x)



def normalize_signal(signal):
    max_abs_value = np.max(np.abs(signal))

    if max_abs_value != 0:
        normalized_signal = signal / max_abs_value
    else:
        normalized_signal = signal

    return normalized_signal

def cross_correlation(x1, x2):
    N = len(x1)
    cross_corr_result = []

    for n in range(N):
        cross_corr_value = 1 / N * sum(x1[j] * x2[(j + n) % N] for j in range(N))
        cross_corr_result.append(cross_corr_value)

    return cross_corr_result


def normalized_cross_correlation(x1, x2):
    N = len(x1)

    if N == 0:
        raise ValueError("Length of signals must be greater than zero.")

    # Calculate the cross-correlation function r12(n)
    cross_corr_result = cross_correlation(x1, x2)

    # Calculate the normalization factor
    norm_factor = (1 / N) * sum(x1[j] ** 2 for j in range(N)) * (1 / N) * sum(x2[j] ** 2 for j in range(N))

    # Check for division by zero
    if norm_factor == 0:
        raise ValueError("Normalization factor is zero. Unable to divide by zero.")

    norm_factor = np.sqrt(norm_factor)

    # Normalize the cross-correlation function
    normalized_corr_result = [r12_n / norm_factor for r12_n in cross_corr_result]

    return normalized_corr_result


def DCT(x):
    N = len(x)
    n = np.arange(N)
    y = np.zeros(N)

    for k in range(N):
        y[k] = np.sum(x * np.cos((np.pi / (4 * N)) * (2 * n - 1) * (2 * k - 1)))
    y *= np.sqrt(2 / N)

    return y


def calculate_mean_correlation(test_file, class_content):
        num_samples = min(len(test_file), len(class_content))
        correlation = np.corrcoef(test_file[:num_samples], class_content[:num_samples])[0, 1]
        return correlation

def decide_correlation(test_file, class1_content, class2_content):
        correlation_class1 = calculate_mean_correlation(test_file, class1_content)
        correlation_class2 = calculate_mean_correlation(test_file, class2_content)

        result_text = f"Average Correlation with Class A: {correlation_class1:.4f}\nAverage Correlation with Class B: {correlation_class2:.4f}"

        if correlation_class1 > correlation_class2:
            result_text += "\nTemplate matches Subject A"
        else:
            result_text += "\nTemplate matches Subject B"

        return result_text

# plotting
def plot_signal(x, y, title):
    fig, ax = plt.subplots() 
    
    ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel('Sample')
    ax.set_ylabel('Amplitude')



