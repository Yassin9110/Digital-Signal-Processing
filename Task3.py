from tkinter import *
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import messagebox, Tk
from tkinter import ttk
import math
from Task3_Test1 import QuantizationTest1
from Task3_Test2 import QuantizationTest2
#SignalSamplesAreEqual(file_name,indices,samples)
Your_EncodedValues = []
Your_QuantizedValues = []

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 3:
                array_size = int(lines[2].strip())
                my_array = [None] * array_size  # Initialize the main array
                x_values = []  # Initialize the x_values array
                y_values = []  # Initialize the y_values array

                for line in lines[3:]:  # Iterate from the fourth line
                    values = line.strip().split()
                    if len(values) >= 2:  # Ensure there are at least 2 values on the line
                        x_value = float(values[0])  # Convert to float
                        y_value = float(values[1])  # Convert to float
                        x_values.append(x_value)  # Append the first value to x_values
                        y_values.append(y_value)  # Append the second value to y_values

                quantize_samples(x_values, y_values)






def quantize_samples(x_values,y_values):
    # Read the samples from the file
    option_of_levels=combo_box.get()
    levels_val =int(Levels_VALUE.get())


    # Determine the range (min and max) of the samples
    min_sample =float(min(y_values))
    max_sample = float(max(y_values))
    levels_intervals=[]
    midpoints=[]
    mapped_values_intervals=[]
    mapped_values_intervals_midpoints = []


    # print("min ",min_sample,"\nmax",max_sample)

    if(option_of_levels=="NUMBER OF LEVELS"):
        # print(min_sample, " \n", max_sample, "\n", levels_val)
        delta = float((max_sample - min_sample)/levels_val)
        num_bits=int(math.log2(levels_val))
    else:
        num_bits = int(levels_val)
        levels_val=int(2**int(levels_val))
        print("levels val: ",levels_val,"\n\n")
        delta = float((max_sample - min_sample) / levels_val)

    inserted_value = min_sample
    value_of_prev_interval = min_sample
    for i in range(0, levels_val):
        inserted_value += float(delta)
        levels_intervals.append((value_of_prev_interval, round(inserted_value, 3)))
        value_of_prev_interval = round(inserted_value, 2)
    # get mid-points of each interval
    midpoints = [round((lower + upper) / 2, 3) for lower, upper in levels_intervals]
    # print(midpoints,"\n")

    # map each value to interval
    # for value in y_values:
    #     for i, (lower, upper) in enumerate(levels_intervals):
    #         if lower <= value <= upper:
    #             mapped_values_intervals.append((value, i))
    #             break  # Exit the loop once the interval is found

    # print(mapped_values_intervals)
    # map values to corresponding midpoint

    for value in y_values:
        for i, (lower, upper) in enumerate(levels_intervals):
            if lower <= value <= upper:
                midpoint = midpoints[i]
                binary = bin(i)[2:].zfill(num_bits)

                error = round((midpoint- value ) , 4)
                mapped_values_intervals_midpoints.append([value, midpoint])
                mapped_values_intervals.append((value, i+1, midpoint, error,binary))
                break  # Exit the loop once the interval is found

    for item in mapped_values_intervals:
        tree.insert("", "end", values=item)
    Your_IntervalIndices = []
    Your_Errors = []
    for item in mapped_values_intervals:
        Inter = item[1]
        Your_EncodedValues.append(item[4])
        Your_QuantizedValues.append(item[2])
        Your_IntervalIndices.append(Inter)
        Your_Errors.append(item[3])

        # Call the test function
        if (option_of_levels == "NUMBER OF LEVELS"):
            QuantizationTest2("Task3\Test 2\Quan2_Out.txt", Your_IntervalIndices, Your_EncodedValues, Your_QuantizedValues, Your_Errors)
        else:
            QuantizationTest1("Task3\Test 1\Quan1_Out.txt", Your_EncodedValues, Your_QuantizedValues)

    # plot_data(x_values, y_values, mapped_values_intervals_midpoints)
    # print(mapped_values_intervals, "\n", mapped_values_intervals_midpoints)

    # for item in mapped_values_intervals:
    #     tree.insert("", "end",values = item)
    # plot_data(x_values, y_values, mapped_values_intervals_midpoints)

def plot_data(x_values, y_values, mapped_values_intervals_midpoints=None):
        plt.figure(figsize=(12, 12))
        # plt.plot(x_values, y_values, label="Signal")
        plt.xlabel("Sample")
        plt.ylabel("Value")
        plt.title("Signal Plot")

        if mapped_values_intervals_midpoints:
            midpoints = [item[1] for item in mapped_values_intervals_midpoints]
            # plt.plot(x_values, midpoints, label="Midpoints")

        # plt.legend()
        # plt.grid(True)
        # plt.show()






      ##################GUI#########################
root = Tk()
root.geometry("600x600")
root.configure(bg="white")
root.title("Quantization of samples")
Levels_label=Label(root ,text="NUMBER OF LEVELS OR BITS" ,fg="black",bg="white")
levels_option=["NUMBER OF LEVELS","NUMBER OF BITS"]
style = ttk.Style()
style.configure("TCombobox", background="black", foreground="darkred")
combo_box =ttk.Combobox(root, values=levels_option,style="TCombobox")
combo_box.set("Select an option")  # Set the default text


Levels_label.place(relx=.33,rely=.2)
combo_box.place(relx=0.33,rely=0.26)

Levels_VALUE=Entry(root,text="",fg="black",font=("bold",12))
Levels_VALUE.place(relx=.31,rely=.35)


upload_button = Button(root, text="Upload File", command=open_file)
upload_button.place(relx=.4,rely=.45)



tree = ttk.Treeview(root, columns=("Value", "Interval", "Quantized", "Error", "Binary"),height=10)
# Set the text for column headers
tree.heading("#1", text="Value")
tree.heading("#2", text="Interval")
tree.heading("#3", text="Quantized")
tree.heading("#4", text="Error")
tree.heading("#5", text="Binary")

# Set the width of columns in the Treeview (if you haven't already done this)
tree.column("#1", width=100)
tree.column("#2", width=100)
tree.column("#3", width=100)
tree.column("#4", width=100)
tree.column("#5", width=100)

# Optionally, you can also adjust the alignment of the columns (e.g., 'center' or 'left')
tree.column("#1", anchor="center")
tree.column("#2", anchor="center")
tree.column("#3", anchor="center")
tree.column("#4", anchor="center")
tree.column("#5", anchor="center")

# Update the Treeview
tree.update()


tree.pack(side="bottom")

root.mainloop()