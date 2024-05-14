import numpy as np
import tkinter as tk
from tkinter import filedialog
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

def design_filter(filter_type, FS, stop_band_attenuation, FC, FC2=None, transition_band=None):
    window_type = calculate_window_type(stop_band_attenuation)
    print("The window type is:", window_type)

    # Step 1: Define the filter type
    if filter_type not in ["Low pass", "High pass", "Band pass", "Band stop"]:
        raise ValueError("Invalid filter type. Choose from 'Low pass', 'High pass', 'Band pass', or 'Band stop'.")

    # Step 2: From stop band attenuation, define the window type
    if window_type not in ["rectangular", "hanning", "hamming", "blackman"]:
        raise ValueError("Invalid window type. Choose from 'rectangular', 'hanning', 'hamming', or 'blackman'.")

    # Step 3: Calculate N from transition width known from the window type
    if transition_band is None:
        raise ValueError("Transition band must be specified.")
    delta_f = transition_band / FS
    N = calculate_samples(window_type, delta_f) 
    if N %2 == 0:
        N += 1
    print("N=", N)

    # Step 4: Calculate the new cut-off frequency
    if filter_type == "Low pass":
        new_fc = FC + 0.5 * transition_band
        print("fc=", new_fc)

        # Normalize cut off frequency
        new_fc = new_fc / FS
        print("The normalized fc=", new_fc)

    elif filter_type == "High pass":
        new_fc = FC - 0.5 * transition_band
        print("fc=", new_fc)

        # Normalize cut off frequency
        new_fc = new_fc / FS
        print("The normalized fc=", new_fc)

    

    elif filter_type == "Band pass":
        new_fc = FC - 0.5 * transition_band
        print("fc1=", new_fc)

        # Normalize cut off frequency
        new_fc = new_fc / FS
        print("The normalized fc1=", new_fc)
        if FC2 is None:
            raise ValueError("For band pass or, FC2 must be specified.")
        new_fc2 = FC2 + 0.5 * transition_band
        print ("fc2=", new_fc2)

        # Normalize cutt off frequency
        new_fc2 = new_fc2 / FS
        print("The normalized fc2=", new_fc2)


    elif filter_type == "Band stop":
        new_fc = FC + 0.5 * transition_band
        print("fc1=", new_fc)

        # Normalize cut off frequency
        new_fc = new_fc / FS
        print("The normalized fc1=", new_fc)
        if FC2 is None:
            raise ValueError("For band reject, FC2 must be specified.")
        new_fc2 = FC2 - 0.5 * transition_band
        print ("fc2=", new_fc2)

        # Normalize cutt off frequency
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
                sinc_term = (((2 * new_fc * np.sin(n * 2 * np.pi * new_fc)) / (n * 2 * np.pi * new_fc)))  # Corrected sinc function
                h_value = sinc_term * window_function(window_type, n, N)
                h.append(h_value)

        elif filter_type == "High pass":
            if i == 0:
                h_value= (1 - 2 * new_fc) * window_function(window_type, n, N)
                h.append(h_value)
            else:
                sinc_term = (((2 * new_fc * np.sin(n * 2 * np.pi * new_fc)) / (n * 2 * np.pi * new_fc)))  # Corrected sinc function
                h_value = -(sinc_term * window_function(window_type, n, N))
                h.append(h_value)

        elif filter_type == "Band pass":
            if i == 0:
                h_value= (2 * (new_fc2 - new_fc)) * window_function(window_type, n, N)
                h.append(h_value)
            else:
                sinc_term1 = (((2 * new_fc * np.sin(n * 2 * np.pi * new_fc)) / (n * 2 * np.pi * new_fc)))  # Corrected sinc function
                sinc_term2 = (((2 * new_fc2 * np.sin(n * 2 * np.pi * new_fc2)) / (n * 2 * np.pi * new_fc2)))  # Corrected sinc function
                total_sincs = sinc_term2 - sinc_term1
                h_value = total_sincs * window_function(window_type, n, N)
                h.append(h_value)

        elif filter_type == "Band stop":
            if i == 0:
                h_value= (1 - (2 * (new_fc2 - new_fc))) * window_function(window_type, n, N)
                h.append(h_value)
            else:
                sinc_term1 = (((2 * new_fc * np.sin(n * 2 * np.pi * new_fc)) / (n * 2 * np.pi * new_fc)))  # Corrected sinc function
                sinc_term2 = (((2 * new_fc2 * np.sin(n * 2 * np.pi * new_fc2)) / (n * 2 * np.pi * new_fc2)))  # Corrected sinc function
                total_sincs = sinc_term1 - sinc_term2
                h_value = total_sincs * window_function(window_type, n, N)
                h.append(h_value)

    # Print the indices and corresponding values
    for i in range(-N // 2 + 1, N // 2 + 1):
        x_values= []
        n = i
        x_values.append(n)
        print(f"{n} {h[i + N // 2]}")

    return x_values , h

# Example usage:
#design_filter("Band stop", FS=1000, stop_band_attenuation=60, FC=150,FC2=250, transition_band=50)



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

    return result


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


#def process_test_files(file_path1):
 #   x_values1, y_values1 = read_file(file_path1)
  #  x_values2, y_values2 = design_filter("Band stop", FS=1000, stop_band_attenuation=60, FC=150, FC2=250, transition_band=50)

   # result = perform_conv(x_values1, y_values1, x_values2, y_values2)

    

      

    

    #plot_convolution(x_values1, y_values1, x_values2, y_values2, x_values, result)







# Example..
#process_test_files("Practical Task\Practical task 1\FIR test cases\Testcase 8\ecg400.txt")





def upsample(signal, factor):
    result = []
    for element in signal:
        result.extend([element] + [0] * (factor - 1))
    for i in range(factor - 1):
        result.pop()
    return result


def resample_signal(file_path, M, L,):
    signal_x, signal_y = read_file(file_path)

    print("The signal x is: ", signal_x)
    print("The signal y is: ", signal_y)
    
    if M == 0 and L != 0:
        # Upsample by inserting L-1 zeros between each sample
        upsampled_signal = upsample(signal_y, L)
        print(upsampled_signal)
        filtered_x, filtered_y = design_filter("Low pass", FS=8000, stop_band_attenuation=50, FC=1500, transition_band=500)
        return perform_conv(signal_x, upsampled_signal, filtered_x, filtered_y)

    elif M != 0 and L == 0:
        # Downsample by taking every Mth sample
        filtered_x, filtered_y = design_filter("Low pass", FS=8000, stop_band_attenuation=50, FC=1500, transition_band=500)
        output_x, output_y = perform_conv(signal_x, signal_y, filtered_x, filtered_y)
        output_x, output_y = output_x[::M], output_y[::M]

        continuous_indices = list(range(min(output_x), min(output_x) + len(output_x)))

        return continuous_indices, output_y

    
    elif M != 0 and L != 0:
        # Upsample, filter, and then downsample
        upsampled_signal = upsample(signal_y, L)
        upsampled_x = upsample(signal_x, L)
        upsampled_x = list(range(min(upsampled_x), min(upsampled_x) + len(upsampled_x)))
        filtered_x, filtered_y = design_filter("Low pass", FS=8000, stop_band_attenuation=50, FC=1500, transition_band=500)
        filtered_signal_x, filtered_signal_y = perform_conv(upsampled_x, upsampled_signal, filtered_x, filtered_y)
        filtered_signal_x, filtered_signal_y = filtered_signal_x[::M], filtered_signal_y[::M]
        print(filtered_signal_y)

        continuous_indices = list(range(min(filtered_signal_x), min(filtered_signal_x) + len(filtered_signal_x)))

        return continuous_indices, filtered_signal_y

    
    



    

    


#Example..design_filter("Low pass", FS=8000, stop_band_attenuation=50, FC=1500, transition_band=500)
resample_signal("Practical Task\Practical task 1\Sampling test cases\Testcase 1\ecg400.txt", M=2, L=0)
    

