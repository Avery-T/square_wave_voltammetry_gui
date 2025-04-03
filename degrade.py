import time
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from potentiostat import Potentiostat
import matplotlib.pyplot as plt
import numpy as np
from helper_code import folders 
from helper_code import plot
Test_Number = 0 
os.chdir("./data")
#start by creating month day folder 
curr_month_day_folder = folders.create_month_day_folder()
os.chdir(curr_month_day_folder) 
Top_Dir = os.getcwd()

def run_test():
								global Top_Dir
								global Test_Number
								os.chdir(Top_Dir ) # always start at the top directory to properly create folders and save files
								# Get user input for test parameters
								try:
																port = port_entry.get()
												#				datafile = filedialog.asksaveasfilename(title="Save Test Data")
												#				if not datafile:
												#												messagebox.showerror("Error", "No file selected for saving data.")
												#												return

																test_name = 'squareWave'
																curr_range = curr_range_var.get()
																sample_rate = float(sample_rate_entry.get())

																test_param = {
																								'quietValue': float(quiet_value_entry.get()),
																								'qietTime': float(quiet_time_entry.get()),
																								'amplitde': float(amplitude_entry.get()),
																								'startValue': float(start_value_entry.get()),
																								'finalValue': float(final_value_entry.get()),
																								'stepValue': float(step_value_entry.get()),
																								'window': float(window_entry.get()),
																}
			 
																# Create potentiostat object and set parameters
																dev = Potentiostat(port)
																dev.set_curr_range(curr_range)
																dev.set_sample_rate(sample_rate)
																dev.set_param(test_name, test_param)

																
																electrode_name = "electrode" + str(electrode_entry.get())  
																save_data_dir =  folders.create_electrode_folder(electrode_name) 
																# will always try to change dir even if it doesnt need to  
																os.chdir(save_data_dir)
																print("got out of electrode")
																test_type = str(test_type_entry.get())
																save_data_dir = folders.create_new_test_set_folder(test_type) 
																os.chdir(save_data_dir)		
																
																for  i in range(100): 
																				print(i) 
																				start_time = time.time() 

																				# Run the test
																				# increment the Test number 
																				Test_Number = Test_Number + 1
																				#test_num_entry.insert(0, Test_Number) 
																				# Initialize lists to store data from multiple runs
																				all_t = []
																				all_volt = []
																				all_curr = []
																				datafile = electrode_name + "_" + test_type  + "_" +"test"+ str( int(test_num_entry.get()) + Test_Number)

																				param_text_name = datafile + ".txt" 

																				with open(param_text_name, 'w') as file:

																								for key, value in test_param.items():
																												file.write(f"{key}:{value}\n") 
																												print(f"{key}: {value}")

																				num_runs = int(average_entry.get())
			 
																				for k in range(num_runs): 
																								print(f"Run {i+1}")
																								t, volt, curr = dev.run_test(test_name, display='pbar', filename=None)
																								all_t.append(t)
																								all_volt.append(volt)
																								all_curr.append(curr)

																				all_t = np.array(all_t)
																				all_volt = np.array(all_volt)
																				all_curr = np.array(all_curr)

																				# Calculate averages
																				avg_t = np.mean(all_t, axis=0)
																				avg_volt = np.mean(all_volt, axis=0)
																				avg_curr = np.mean(all_curr, axis=0)
												 
																				#get the time in buffer 
																				minutes_in_buffer =  float(minutes_in_buffer_entry.get())
																				# create array with the same size 

																				minutes_in_buffer_array = np.zeros_like(avg_t) 

																				minutes_in_buffer_array[0] = i * 2
																				print(minutes_in_buffer_array[0])

																				csv_data = np.column_stack((avg_t,avg_volt,avg_curr,minutes_in_buffer_array)) 

																				# Save Data to a CSV file 
																				csv_filename = datafile + ".csv"
																				np.savetxt(csv_filename, csv_data, delimiter=",",header="time,volts,current,minutes_in_buffer",comments="",fmt="%f")


																				data_file = datafile + ".png"

																				# Plot averaged results
																				plt.figure(1)
																				plt.subplot(211)
																				plt.plot(avg_t, avg_volt)
																				plt.ylabel('potential (V)')
																				plt.grid('on')

																				plt.subplot(212)
																				plt.plot(avg_t, avg_curr)
																				plt.ylabel('current (uA)')
																				plt.xlabel('time (sec)')
																				plt.grid('on')
				

																				plt.savefig(data_file,dpi=600, bbox_inches='tight')
																				plt.clf()
																				data_file = datafile + "_.png"
																				plt.figure(2)
																				plt.plot(avg_volt, avg_curr)
																				plt.xlabel('potential (V)')
																				plt.ylabel('current (uA)')
																				plt.grid('on')
																				plt.savefig(data_file,dpi=600, bbox_inches='tight')
																				plt.clf()
																				#plt.show()

												#								messagebox.showinfo("Success", "Test completed and data saved.")
																				end_time = time.time()
																				print(end_time) 
																				print(start_time) 
																				sleep_time = 120 - (end_time -start_time) 
																				# to block sleeping on the last iteration
																				if( i != 5):
																						"time.sleep(sleep_time)" 




								except Exception as e:
																messagebox.showerror("Error", f"An error occurred: {e}")
																end_time = time.time() 
																#2 minute intervals
																# Create the main tkinter window
root = tk.Tk()
root.title("Squarewave Voltammetry")

# Default parameters 
default_params = {
								'port': '/dev/ttyACM0',
								'curr_range': '100uA',
								'sample_rate': 100.0,
								'quietValue': 0,
								'qietTime': 0,
								'amplitde': 0.025,
								'startValue': -0.6,
								'finalValue': 0,
								'stepValue': 0.001,
								'window': 0.05,
								'avg_amount': 1,
								'electrode':0,	
		'test_num':0, 
								'test_type': 'buffer', 
								'minutes_in_buffer': 0.0
}


# Create input fields
fields = ["Port","Electrode","Test Number", "Test Type","Minutes In Buffer" "Current Range", "Sample Rate", "Quiet Value", "Quiet Time", "Amplitude", "Start Value", "Final Value", "Step Value", "Window","Average Amount"] 
entries = {}

port_entry = tk.Entry(root, width=30)
port_entry.insert(0, default_params['port'])
entries['Port'] = port_entry

curr_range_var = tk.StringVar(value=default_params['curr_range'])
curr_range_menu = tk.OptionMenu(root, curr_range_var, "100uA", "1mA", "10mA")

electrode_entry = tk.Entry(root, width=30)
electrode_entry.insert(0, default_params['electrode'])
entries['Electrode'] = electrode_entry 

test_num_entry = tk.Entry(root, width=30)
test_num_entry.insert(0, default_params['test_num'])
entries['Test Number'] = test_num_entry 

test_type_entry = tk.Entry(root, width=30)
test_type_entry.insert(0, default_params['test_type'])
entries['Test Type'] = test_type_entry 

minutes_in_buffer_entry = tk.Entry(root, width=30)
minutes_in_buffer_entry.insert(0, default_params['minutes_in_buffer'])
entries['Minutes In Buffer'] = minutes_in_buffer_entry 

sample_rate_entry = tk.Entry(root, width=30)
sample_rate_entry.insert(0, default_params['sample_rate'])
entries['Sample Rate'] = sample_rate_entry

quiet_value_entry = tk.Entry(root, width=30)
quiet_value_entry.insert(0, default_params['quietValue'])
entries['Quiet Value'] = quiet_value_entry

quiet_time_entry = tk.Entry(root, width=30)
quiet_time_entry.insert(0, default_params['qietTime'])
entries['Quiet Time'] = quiet_time_entry

amplitude_entry = tk.Entry(root, width=30)
amplitude_entry.insert(0, default_params['amplitde'])
entries['Amplitude'] = amplitude_entry

start_value_entry = tk.Entry(root, width=30)
start_value_entry.insert(0, default_params['startValue'])
entries['Start Value'] = start_value_entry

final_value_entry = tk.Entry(root, width=30)
final_value_entry.insert(0, default_params['finalValue'])
entries['Final Value'] = final_value_entry

step_value_entry = tk.Entry(root, width=30)
step_value_entry.insert(0, default_params['stepValue'])
entries['Step Value'] = step_value_entry

window_entry = tk.Entry(root, width=30)
window_entry.insert(0, default_params['window'])
entries['Window'] = window_entry

average_entry = tk.Entry(root, width=30)
average_entry.insert(0, default_params['avg_amount'])
entries['Average Amount'] = average_entry

plot_entry = tk.Entry(root, width=30)
plot_entry.insert(20, default_params['avg_amount'])


# Arrange fields in the window

tk.Label(root, text="Port").grid(row=0, column=0, padx=5, pady=5)
port_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Current Range").grid(row=1, column=0, padx=5, pady=5)
curr_range_menu.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Electrode").grid(row=2, column=0, padx=5, pady=5)
electrode_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Starting Test Number").grid(row=3, column=0, padx=5, pady=5)
test_num_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Test Type").grid(row=4, column=0, padx=5, pady=5)
test_type_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Minutes In Buffer").grid(row=5, column=0, padx=5, pady=5)
minutes_in_buffer_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Sample Rate").grid(row=6, column=0, padx=5, pady=5)
sample_rate_entry.grid(row=6, column=1, padx=5, pady=5)

tk.Label(root, text="Quiet Value").grid(row=7, column=0, padx=5, pady=5)
quiet_value_entry.grid(row=7, column=1, padx=5, pady=5)

tk.Label(root, text="Quiet Time").grid(row=8, column=0, padx=5, pady=5)
quiet_time_entry.grid(row=8, column=1, padx=5, pady=5)

tk.Label(root, text="Amplitude").grid(row=9, column=0, padx=5, pady=5)
amplitude_entry.grid(row=9, column=1, padx=5, pady=5)

tk.Label(root, text="Start Value").grid(row=10, column=0, padx=5, pady=5)
start_value_entry.grid(row=10, column=1, padx=5, pady=5)

tk.Label(root, text="Final Value").grid(row=11, column=0, padx=5, pady=5)
final_value_entry.grid(row=11, column=1, padx=5, pady=5)

tk.Label(root, text="Step Value").grid(row=12, column=0, padx=5, pady=5)
step_value_entry.grid(row=12, column=1, padx=5, pady=5)

tk.Label(root, text="Window").grid(row=13, column=0, padx=5, pady=5)
window_entry.grid(row=13, column=1, padx=5, pady=5)

tk.Label(root, text="Averaging Amount").grid(row=14, column=0, padx=5, pady=5)
average_entry.grid(row=14, column=1, padx=5, pady=5)

# Run button
run_button = tk.Button(root, text="Run Test", command=run_test)
run_button.grid(row=15, column=0, columnspan=2, pady=10)

# Run button
plot_button = tk.Button(root, text="Plot a Days Data", command=lambda: plot.plot_data(plot_entry.get()))
plot_button.grid(row=16, column=1, columnspan=2, pady=10)

# Entry widget
plot_entry = tk.Entry(root, width=30)
plot_entry.insert(0, curr_month_day_folder[2:])  # removed the ./ to make it easier to understand for users 
plot_entry.grid(row=16, column=0, padx=10, pady=10)  # Position it next to the button


# Start the Tkinter event loop
root.mainloop()


# Start the Tkinter event loop
root.mainloop()


