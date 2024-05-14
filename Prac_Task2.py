import os
import numpy as np
from scipy.signal import firwin, lfilter, resample, correlate
from scipy.fftpack import dct
import matplotlib.pyplot as plt

def distinguish_subjects(ecg_folder_A, ecg_folder_B, test_file, Fs, miniF, maxF, newFs):
    def load_ecg_files(folder):
        ecg_files = os.listdir(folder)
        ecg_data = [np.loadtxt(os.path.join(folder, file)) for file in ecg_files]
        return ecg_data

    def filter_signal(signal, Fs, miniF, maxF):
        nyquist = 0.5 * Fs
        low = miniF / nyquist
        high = maxF / nyquist
        taps = 101  # Adjust the filter length as needed
        coefficients = firwin(taps, [low, high], pass_zero=False)
        filtered_signal = lfilter(coefficients, 1.0, signal)
        return filtered_signal

    def resample_signal(signal, Fs, newFs):
        try:
            resampled_signal = resample(signal, int(len(signal) * newFs / Fs))
            return resampled_signal
        except ValueError:
            print("newFs is not valid. Continuing with the original signal.")
            return signal

    def remove_dc_component(signal):
        return signal - np.mean(signal)

    def normalize_signal(signal):
        return 2 * (signal - np.min(signal)) / (np.max(signal) - np.min(signal)) - 1

    def compute_auto_correlation(signal):
        correlation = correlate(signal, signal, mode='full')
        return correlation[len(correlation)//2:]

    def preserve_auto_correlation_coefficients(auto_correlation, num_coefficients):
        return auto_correlation[:num_coefficients]

    def compute_dct(signal):
        return dct(signal, norm='ortho')

    def template_matching(dct_A, dct_B, test_dct):
        distance_A = np.linalg.norm(test_dct - dct_A)
        distance_B = np.linalg.norm(test_dct - dct_B)

        if distance_A < distance_B:
            return 'A'
        else:
            return 'B'

    # Load ECG signals from folders
    ecg_A = load_ecg_files(ecg_folder_A)
    ecg_B = load_ecg_files(ecg_folder_B)

    # Process the test file
    test_ecg = np.loadtxt(test_file)

    # Filter, resample, remove DC, and normalize test ECG signal
    filtered_test = normalize_signal(remove_dc_component(resample_signal(filter_signal(test_ecg, Fs, miniF, maxF), Fs, newFs)))

    # Compute auto-correlation for test signal
    auto_corr_test = compute_auto_correlation(filtered_test)

    # Preserve auto-correlation coefficients for test signal
    num_coefficients = 10  # Adjust as needed
    preserved_auto_corr_test = preserve_auto_correlation_coefficients(auto_corr_test, num_coefficients)

    # Compute DCT for test signal
    dct_test = compute_dct(preserved_auto_corr_test)

    # Display signals and labels for the test file
    plt.figure(figsize=(12, 8))

    plt.subplot(411)
    plt.plot(test_ecg, label='Test Signal')
    plt.title('Original Test Signal')

    plt.subplot(412)
    plt.plot(auto_corr_test, label='Test Signal')
    plt.title('Auto-correlation of Test Signal')

    plt.subplot(413)
    plt.plot(preserved_auto_corr_test, label='Test Signal')
    plt.title('Preserved Auto-correlation of Test Signal')

    plt.subplot(414)
    plt.plot(dct_test, label='Test Signal')
    plt.title('DCT of Test Signal')

    plt.show()

    # Template matching and label the test ECG segment
    label = template_matching(
        compute_dct(preserve_auto_correlation_coefficients(
            compute_auto_correlation(
                normalize_signal(
                    remove_dc_component(
                        resample_signal(
                            filter_signal(ecg_A[0], Fs, miniF, maxF), Fs, newFs
                        )
                    )
                )
            ),
            num_coefficients=10
        )),
        compute_dct(preserve_auto_correlation_coefficients(
            compute_auto_correlation(
                normalize_signal(
                    remove_dc_component(
                        resample_signal(
                            filter_signal(ecg_B[0], Fs, miniF, maxF), Fs, newFs
                        )
                    )
                )
            ),
            num_coefficients=10
        )),
        dct_test
    )

    print(f"The test signal is predicted to belong to Subject {label}.")


# Example usage:
distinguish_subjects("Practical Task\Practical task 2\A", "Practical Task\Practical task 2\B", "Practical Task\Practical task 2\Test Folder\BTest1.txt", Fs=1000, miniF=0.5, maxF=50, newFs=500)
