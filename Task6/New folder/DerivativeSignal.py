import matplotlib.pyplot as plt

def DerivativeSignal():
    InputSignal = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 40.0, 41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0, 80.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 87.0, 88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0]
    expectedOutput_first = [1.0] * 98
    expectedOutput_second = [0.0] * 97  # Adjusted length to match the calculated second derivative


    """
    Write your Code here:
    Start
    """
    FirstDrev = [InputSignal[i] - InputSignal[i - 1] for i in range(1, len(InputSignal))]
    SecondDrev = [InputSignal[i + 1] - 2 * InputSignal[i] + InputSignal[i - 1] for i in range(1, len(InputSignal) - 1)]

    """
    End
    """

    # Plotting
    plt.figure(figsize=(12, 6))

    plt.subplot(3, 1, 1)
    plt.plot(InputSignal, label='Original Signal')
    plt.title('Original Signal')
    plt.xlabel('Sample Index')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(FirstDrev, label='First Derivative')
    plt.title('First Derivative')
    plt.xlabel('Sample Index')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(SecondDrev, label='Second Derivative')
    plt.title('Second Derivative')
    plt.xlabel('Sample Index')
    plt.legend()

    plt.tight_layout()
    plt.show()

    """
    Testing your Code
    """
    if (len(FirstDrev) != len(expectedOutput_first)) or (len(SecondDrev) != len(expectedOutput_second)):
        print("Mismatch in length")
        return
    first = second = True
    for i in range(len(expectedOutput_first)):
        if abs(FirstDrev[i] - expectedOutput_first[i]) < 0.01:
            continue
        else:
            first = False
            print("1st derivative wrong")
            return
    for i in range(len(expectedOutput_second)):
        if abs(SecondDrev[i] - expectedOutput_second[i]) < 0.01:
            continue
        else:
            second = False
            print("2nd derivative wrong")
            return
    if first and second:
        print("Derivative Test case passed successfully")
    else:
        print("Derivative Test case failed")
    return


DerivativeSignal()
